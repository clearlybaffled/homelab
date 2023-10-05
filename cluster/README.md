<h1><p align="center">
<a href="https://argoproj.github.io/cd"><img src="https://api.iconify.design/logos/argo.svg?height=250" ></a></h1>
<br/><br/><img src="https://img.shields.io/github/v/release/argoproj/argo-cd?label=Latest%20Version&logo=github&style=for-the-badge">
</p>

## Motivation

After learning about the existence of GitOps, combining that with what I knew about Kubernetes and Helm,
I decided to have exactly one requirement for my GitOps solution, and that's pretty much driven many of the design decisions that have gotten me here:

> Applications should be able to be installed into a cluster without any assistance from the GitOps tool.

Flux did not seem to meet this requirement, as they have a CRD called `HelmRelease` that bundles all the information necessary to deploy the chart into one (custom) file,
and the only way to separate out the values from the HelmRelease file is to put them into a `ConfigMap` or `Secret`.  Flux also seemed to have a lot of boilerplate yaml that seemed .. unnecessary.

After some googling, I came across ArgoCD as the other "big" GitOps solution in the cloud-native world.
After several iterations of structuring the cluster directories in order to both work well and meet my requirement, I've landed on this current setup.

## Setup

The directory layout below mimics the one found in many of the other k8s-at-home users (descending from [onedr0p's template](https://github.com/onedr0p/flux-cluster-template)
most likely) which has a top level `kubernetes` folder and subdirectories for `apps`,`bootstrap`, and `flux`.

### Directory Structure

```console
$ tree cluster -P cluster.yaml
cluster
├──apps
│   ├── db
│   │   ├── cloudnative-pg
|   |   ├── mysql
│   │   └── ...
│   ├── home
│   │   ├── grocy
│   │   ├── hajimari
│   │   └── ...
│   ├── infrastructure
│   │   ├── cert-manager
│   │   ├── ingress-nginx
│   │   └── ...
│   ├── media
│   │   ├── calibre
│   │   ├── immich
│   │   └── ...
│   └── monitoring
│       └── kube-prometheus-stack
├── argocd
├── manifests
│   ├── db
│   ├── home
│   ├── infrastructure
│   ├── media
|   ├── monitoring
|   └── argocd.yaml
└── cluster.yaml
```

- `cluster.yaml` implements the ArgoCD app-of-apps pattern and applies everything under the `cluster/manifests`
- `cluster/manifests` directory contains all of the ArgoCD Application YAML files, organized by namespace.
Each ArgoCD application points to the respective subdirectory in `cluster/apps/{namespace}/{app.name}` that ArgoCD needs to load files from and monitor for changes.
- `cluster/apps` has all of the application specific configuration files, like `values.yaml`, `kustomization.yaml`, and other kubernetes yaml manifest and custom resource files.
- `cluster/argocd` is the configuration for the ArgoCD gitops sub-system itself

I tried getting rid of the `bootstrap` directory and putting all of the  `Application` files in each `cluster/apps/...` directory,
but found that because of the finalizer on the Application object itself combined with the fact that each Application contained itself as a component, it created a deadlock in deletion. So I renamed the `bootstrap` directory to `manifests` and continued on.

### Populating `cluster/manifests`

