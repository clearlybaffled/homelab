import os
import yaml
from urllib.parse import urlparse

from ansible.parsing.yaml.dumper import AnsibleDumper
from ansible.module_utils.common.text.converters import to_native, to_text
from ansible.errors import AnsibleFilterError

from jinja2.filters import pass_context

def get_helm_chart_repo(chart, app_name, helm_repositories):
    if chart["chart"] == "app-template":
        chart_name = chart["chart"]
        helm_repo = "bjw-s"
    else:
        try:
            parse_result = urlparse(chart["chart"])
            if parse_result.scheme == "":
                (helm_repo, chart_name) = parse_result.path.split("/")
            else:
                return (chart["chart"], app_name)
        except ValueError:
            (helm_repo, chart_name) = chart["chart"].split("/")

    return (helm_repositories[helm_repo], chart_name)


def helm_charts(charts, app, helm_repos, app_template_version):
    chart_list = []
    for chart in charts:
        (repo_url, chart_name) = get_helm_chart_repo(chart, app["name"], helm_repos)

        c = {
            "name": chart_name,
            "repo_url": repo_url,
        }

        if chart_name == "app-template":
            c["version"] = app_template_version
        else:
            c["version"] = chart["version"]

        if "release" in chart:
            c["release_name"] = chart["release"]
        elif app["name"] != chart_name and chart_name != "app-template":
            c["release_name"] = chart_name
        else:
            c["release_name"] = app["name"]

        if "namespace" in chart:
            c["namespace"] = chart["namespace"]
        else:
            c["namespace"] = app["namespace"]

        if "valueFiles" in chart:
            if chart["valueFiles"]:
                c["value_files"] = chart["valueFiles"]
        else:
            c["value_files"] = ["values.yaml"]

        if "skipCrds" in chart:
            c["skip_crds"] = bool(chart["skipCrds"])
        else:
            c["skip_crds"] = False

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

    repo_dir = (
        os.path.relpath(app["app_dir"]) if os.path.exists(app["app_dir"]) else None
    )

    if repo_dir:
        repo_source = {
            "repoURL": (
                app["repo_url"] if "repo_url" in app else ctx.get("git_repo_url")
            ),
            "path": repo_dir,
            "targetRevision": ctx.get("git_branch"),
        }

    if "charts" in app:
        for chart in helm_charts(
            app["charts"],
            app,
            ctx.get("helm_repositories"),
            ctx.get("app_template_version"),
        ):
            source = {
                "chart": chart["name"],
                "repoURL": chart["repo_url"],
                "targetRevision": chart["version"],
            }
            helm = {}
            if chart["skip_crds"]:
                helm["skipCrds"] = chart["skip_crds"]

            if "value_files" in chart and repo_dir:
                helm["valueFiles"] = [
                    os.path.join("$repo", repo_dir, file)
                    for file in chart["value_files"]
                ]
                repo_source["ref"] = "repo"

            if "release_name" in chart:
                helm["releaseName"] = chart["release_name"]

            if helm:
                source["helm"] = helm

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
        raise AnsibleFilterError(
            "application - No sources provided for application %s. Add a source or create the %s directory"
            % (app["name"], app["app_dir"])
        )

    spec["destination"] = {"name": "in-cluster", "namespace": app["namespace"]}

    if "localStorage" in app:
        spec["ignoreDifferences"] = [
            {
                "kind": "PersistentVolume",
                "jsonPointers": [
                    "/spec/claimRef/resourceVersion",
                    "/spec/claimRef/uid",
                    "/status/lastPhaseTransitionTime",
                ],
            }
        ]
    if "ignoreDifferences" in app:
        if "ignoreDifferences" in spec:
            for i in app["ignoreDifferences"]:
                spec["ignoreDifferences"].append(i)
        else:
            spec["ignoreDifferences"] = app["ignoreDifferences"]

    spec["syncPolicy"] = {
        "automated": {"prune": True, "selfHeal": True},
        "syncOptions": ["CreateNamespace=true", "ServerSideApply=true"],
    }

    if "ignoreDifferences" in spec:
        spec["syncPolicy"]["syncOptions"].append("RespectIgnoreDifferences=true")

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

    resources = []

    if "kustomize" in app:
        if "resources" in app["kustomize"]:
            resources += [r for r in app["kustomize"]["resources"]]

        if "charts" in app["kustomize"]:
            kustomize.update({"helmCharts": []})
            for chart in helm_charts(
                app["kustomize"]["charts"],
                app,
                ctx.get("helm_repositories"),
                ctx.get("app_template_version"),
            ):
                c = {
                    "name": chart["name"],
                    "repo": chart["repo_url"],
                    "version": chart["version"],
                    "namespace": chart["namespace"],
                }

                if "apiVersions" in chart and chart["apiVersions"]:
                    c["apiVersions"] = ctx.get("k8s_apis")

                if "release_name" in chart:
                    c["releaseName"] = chart["release_name"]

                if chart["skip_crds"]:
                    c["includeCRDs"] = not chart["skip_crds"]

                if "value_files" in chart:
                    c["valuesFile"] = chart["value_files"][0]
                    if len(chart["value_files"]) > 1:
                        c["additionalValuesFiles"] = chart["value_files"][1:]

                kustomize["helmCharts"].append(c)

        if "extras" in app["kustomize"]:
            kustomize.update(app["kustomize"]["extras"])

    if "localStorage" in app:
        resources.append("./storage.yaml")
    resources.sort()
    if resources:
        kustomize.update({"resources": resources})

    try:
        transformed = yaml.dump(
            kustomize,
            Dumper=AnsibleDumper,
            sort_keys=False,
            indent=2,
            allow_unicode=True,
        )
    except Exception as e:
        raise AnsibleFilterError("kustomization - %s" % to_native(e), orig_exc=e)
    return to_text(transformed)


def pvc(app, dir):
    p = {
        "apiVersion": "v1",
        "kind": "PersistentVolumeClaim",
        "metadata": {
            "name": dir["name"],
            "namespace": app["namespace"],
            "finalizers": ["kubernetes.io/pvc-protection"]
        },
        "spec": {
            "accessModes": dir["modes"],
            "resources": {"requests": {"storage": dir["size"]}},
            "storageClassName": "local-storage",
            "volumeName": dir["name"],
        },
    }

    return p


def pv(app, dir):
    pv = {
        "apiVersion": "v1",
        "kind": "PersistentVolume",
        "metadata": {
            "name": dir["name"],
            "finalizers": ["kubernetes.io/pv-protection"]
        },
        "spec": {
            "accessModes": dir["modes"],
            "claimRef": {
                "apiVersion": "v1",
                "kind": "PersistentVolumeClaim",
                "name": dir["name"],
                "namespace": app["namespace"],
            },
            "persistentVolumeReclaimPolicy": "Retain",
            "volumeMode": "Filesystem",
            "storageClassName": "local-storage",
            "capacity": {"storage": dir["size"]},
            "local": {"path": dir["path"]},
            "nodeAffinity": {
                "required": {
                    "nodeSelectorTerms": [
                        {
                            "matchExpressions": [
                                {
                                    "key": "kubernetes.io/hostname",
                                    "operator": "In",
                                    "values": ["parche"],
                                }
                            ]
                        }
                    ]
                }
            },
        },
    }
    return pv


@pass_context
def storage(ctx, app):
    pvcs = []
    pvs = []
    for dir in ctx.get("storage_dirs"):
        pvs.append(pv(app, dir))
        pvcs.append(pvc(app, dir))
    pvcs.sort(key=lambda x: x["metadata"]["name"])
    pvs.sort(key=lambda x: x["metadata"]["name"])

    try:
        transformed = yaml.dump_all(
            pvs + pvcs,
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
        return {
            "application": application,
            "kustomization": kustomization,
            "storage": storage,
        }
