<p align="center">
<a href="https://argo-cd.readthedocs.org"><img src="https://api.iconify.design/logos/argo.svg?height=250"></a>



```console
$ tree . -P bootstrap.yaml
.
├── apps
│   ├── db
│   │   ├── cloudnative-pg
│   │   ├── mysql
│   │   ├── redis
│   │   └── typesense
│   ├── home
│   │   ├── grocy
│   │   ├── hajimari
│   │   ├── heimdall
│   │   ├── mealie
│   │   ├── nextcloud
│   │   ├── paperless-ngx
│   │   ├── photonix
│   │   └── qbittorrent
│   ├── infrastructure
│   │   ├── cert-manager
│   │   ├── ingress-nginx
│   │   ├── metallb
│   │   ├── netbox
│   │   ├── rook-ceph
│   │   └── vault
│   ├── media
│   │   ├── calibre
│   │   ├── immich
│   │   ├── lidarr
│   │   ├── listen-brainz
│   │   ├── overseerr
│   │   ├── photonix
│   │   ├── prowlarr
│   │   ├── radarr
│   │   ├── readarr
│   │   └── sonarr
│   └── monitoring
│       └── kube-prometheus-stack
├── argocd
├── bootstrap
│   ├── db
│   ├── home
│   ├── infrastructure
│   ├── media
|   ├── monitoring   
|   └── argocd.yaml
└── bootstrap.yaml
```

- `bootstrap.yaml` implements the ArgoCD app-of-apps pattern, recurses througth `cluster/bootstrap` directory and applies all of the ArgoCD Application YAML files inside, organized by namespace
- `cluster/apps` has all of the application specific configuration files, like `values.yaml` for helm charts, and other kubernetes yaml manifest files. Each ArgoCD application points to the respective subdirectory in `cluster/apps/{namespace}/{appname}` and loads all of those files.
- `cluster/argocd` is the configuration for the ArgoCD gitops sub-system itself
- This directory layout mimics the one found in many of the other k8s-at-home users (descending from onedr0p's template most likely) which has a top level `kubernetes` folder and subdirectories for `apps`,`bootstrap`, and `flux`. I tried getting rid of the `bootstrap` directory and putting `application.yaml` files in each `cluster/apps/...` directory, but found that because of the finalizer on the Application object itself combined with the fact that the Application contained itself as a component, created a deadlock in deletion.