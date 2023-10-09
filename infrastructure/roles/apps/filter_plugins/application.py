import os
import yaml
from urllib.parse import urlparse

from ansible.parsing.yaml.dumper import AnsibleDumper
from ansible.module_utils.common.text.converters import to_native, to_text
from ansible.errors import AnsibleFilterError

from jinja2.filters import pass_context


def get_helm_chart_repo(chart, app_name, helm_repositories):
    try:
        parse_result = urlparse(chart["chart"])
        if parse_result.scheme == '':
            (helm_repo, chart_name) = parse_result.path.split("/")
        else:
            return (chart["chart"], app_name)
    except ValueError:
        (helm_repo, chart_name) = chart["chart"].split("/")

    return (helm_repositories[helm_repo], chart_name)


def helm_charts(charts, app, helm_repos):
    chart_list = []
    for chart in charts:
        (repo_url, chart_name) = get_helm_chart_repo(
            chart, app["name"], helm_repos)

        c = {
            'name': chart_name,
            'repo_url': repo_url,
            "version": chart["version"],
            'skip_crds': bool(chart["skipCrds"]) if "skipCrds" in chart else False
        }

        if "release" in chart:
            c['release_name'] = chart["release"]
        elif app['name'] != chart_name:
            c['release_name'] = chart_name

        if "namespace" in chart:
            c['namespace'] = chart["namespace"]
        else:
            c['namespace'] = app["namespace"]

        if "valueFiles" in chart:
            if chart["valueFiles"]:
                c['value_files'] = chart["valueFiles"]
        else:
            c['value_files'] = ['values.yaml']

        chart_list.append(c)

    return chart_list


@pass_context
def application(ctx, app):
    metadata = {
        "name": app["name"],
        "namespace": "argocd",
        "finalizers": ["resources-finalizer.argocd.argoproj.io"],
    }

    if "wave" in app:
        metadata["annotations"] = {"argocd.argoproj.io/sync-wave": app["wave"]}

    spec = {"project": "default"}

    sources = []

    repo_dir = os.path.relpath(app["app_dir"]) if os.path.exists(app["app_dir"]) else None

    if repo_dir:
        repo_source = {
            "repoURL": app["repo_url"] if "repo_url" in app else ctx.get("git_repo_url"),
            "path": repo_dir,
            "targetRevision": ctx.get("git_branch"),
        }

    if "charts" in app:
        for chart in helm_charts(app["charts"], app, ctx.get("helm_repositories")):
            source = {
                "chart": chart['name'],
                "repoURL": chart['repo_url'],
                "targetRevision": chart["version"]
            }
            helm = {}
            if chart["skip_crds"]:
                helm["skipCrds"] = chart["skip_crds"]

            if 'value_files' in chart and repo_dir:
                helm['valueFiles'] = [ os.path.join("$repo", repo_dir, file) for file in chart["value_files"] ]
                repo_source["ref"] = "repo"

            if 'release_name' in chart:
                helm["releaseName"] = chart["release_name"]

            if helm:
                source['helm'] = helm

            sources.append(source)

    if repo_dir:
        if "directory" in app:
            repo_source.update({"directory": app["directory"]})

        sources.append(repo_source)

    if len(sources) > 1:
        spec.update({"sources": sources})
    elif len(sources) == 1:
        spec.update({"source": sources[0]})
    else:
        raise AnsibleFilterError("application - No sources provided for application %s. Add a source or create the %s directory" % (app["name"], app["app_dir"]))

    spec["destination"] = {"name": "in-cluster", "namespace": app["namespace"]}

    if "pv" in app and app["pv"]:
        spec["ignoreDifferences"] = [
                    {
                        "kind": "PersistentVolume",
                        "jsonPointers": [
                            "/spec/claimRef/resourceVersion",
                            "/spec/claimRef/uid"
                        ]
                    }
                ]

    spec["syncPolicy"] = {
                "automated": {"prune": True, "selfHeal": True },
                "syncOptions": ["CreateNamespace=true", "ServerSideApply=true"] }

    if "pv" in app and app["pv"]:
        spec["syncPolicy"]["syncOptions"].append(
            "RespectIgnoreDifferences=true")

    application = {
        "apiVersion": "argoproj.io/v1alpha1",
        "kind": "Application",
        "metadata": metadata,
        "spec": spec,
    }
    try:
        transformed = yaml.dump(
            application,
            Dumper=AnsibleDumper,
            sort_keys=False,
            indent=2,
            allow_unicode=True,
            default_flow_style=False,
        )
    except Exception as e:
        raise AnsibleFilterError("application - %s" % to_native(e), orig_exc=e)
    return to_text(transformed)


@pass_context
def kustomization(ctx, app):
    kustomize = {
        "apiVersion": "kustomize.config.k8s.io/v1beta1",
        "kind": "Kustomization",
        "namespace": app["namespace"],
    }

    if "secrets" in app:
        kustomize.update({"generators": ["./secret-generator.yaml"]})

    if "kustomize" in app:
        if "resources" in app["kustomize"]:
            kustomize.update(
                {"resources": [r for r in app["kustomize"]["resources"]]})

        if "charts" in app["kustomize"]:
            helm_repositories = ctx.get("helm_repositories")
            kustomize.update({"helmCharts": []})
            for chart in helm_charts(app["kustomize"]["charts"], app, ctx.get("helm_repositories")):
                c = {
                    "name": chart["name"],
                    "repo": chart["repo_url"],
                    "version": chart["version"],
                    "namespace": chart["namespace"],
                }

                if 'release' in chart:
                    c["release_name"] = chart["release"]

                if chart["skip_crds"]:
                    c["includeCRDs"] = not chart["skip_crds"]

                if "values_files" in chart:
                    c["valuesFile"] = chart["values_files"][0]
                    if len(chart["values_files"]) > 1:
                        c["additionalValuesFiles"] = chart["values_files"][1:]

                kustomize["helmCharts"].append(c)

        if "extras" in app["kustomize"]:
            kustomize.update(app["kustomize"]["extras"])

    try:
        transformed = yaml.dump(
            kustomize,
            Dumper=AnsibleDumper,
            sort_keys=False,
            indent=2,
            allow_unicode=True,
            default_flow_style=False,
        )
    except Exception as e:
        raise AnsibleFilterError("kustomization - %s" %
                                 to_native(e), orig_exc=e)
    return to_text(transformed)


def pvc(app):
    pvcs = []
    for pvc in app["pvc"]:
        p = {
            "apiVersion": "v1",
            "kind": "PersistentVolumeClaim",
            "metadata": {"name": pvc["name"], "namespace": app["namespace"]},
            "finalizers": ["kubernetes.io/pvc-protection"],
            "spec": {
                "accessModes": [
                    pvc["accessMode"] if "accessMode" in pvc else "ReadWriteMany"
                ],
                "resources": {"requests": {"storage": pvc["size"]}},
            },
        }
        if "storageClass" in pvc:
            p['spec'].update({"storageClassName": pvc["storageClass"]})
        if "volumeName" in pvc:
            p['spec'].update({"volumeName": pvc["volumeName"]})
        pvcs.append(p)
    try:
        transformed = yaml.dump_all(
            pvcs,
            Dumper=AnsibleDumper,
            sort_keys=False,
            indent=2,
            allow_unicode=True,
            default_flow_style=False,
        )
    except Exception as e:
        raise AnsibleFilterError("pvc - %s" % to_native(e), orig_exc=e)
    return to_text(transformed)


class FilterModule(object):
    def filters(self):
        return {"application": application, "kustomization": kustomization, "pvc": pvc}
