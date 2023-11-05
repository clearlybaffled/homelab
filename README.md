<h1 tabindex="-1" dir="auto" style="bottom-border:none;"><img src="https://camo.githubusercontent.com/5b298bf6b0596795602bd771c5bddbb963e83e0f/68747470733a2f2f692e696d6775722e636f6d2f7031527a586a512e706e67" width="144px" height="144px" align="left"/>

<!-- markdownlint-disable-next-line MD013 -->
<a id="user-content-homelab" class="anchor" aria-hidden="true" href="#homelab"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a>
Homelab
</h1>

> K8S cluster built with Ansible and managed using ArgoCD for GitOps

<div align="center">

[![Discord](https://img.shields.io/badge/discord-chat-7289DA.svg?maxAge=60&style=flat-square&logo=discord)](https://discord.gg/DNCynrJ)&nbsp;&nbsp;&nbsp;
[![k8s](https://img.shields.io/badge/k8s-v1.28.2-blue?style=flat-square&logo=kubernetes)](https://k8s.io/)&nbsp;&nbsp;&nbsp;
[![debian](https://img.shields.io/badge/debian-bookworm-C70036?style=flat-square&logo=debian&logoColor=C70036)](https://debian.org)&nbsp;&nbsp;&nbsp;
[![GitHub last commit](https://img.shields.io/github/last-commit/clearlybaffled/homelab/main?style=flat-square&logo=git&color=F05133)](https://github.com/clearlybaffled/homelab/commits/main)

[![WTFPL](https://img.shields.io/github/license/clearlybaffled/homelab?style=flat-square&color=darkred)](http://www.wtfpl.net/)&nbsp;&nbsp;&nbsp;
[![Linters](https://github.com/clearlybaffled/homelab/actions/workflows/linters.yaml/badge.svg)](https://github.com/clearlybaffled/homelab/actions/workflows/linters.yaml)&nbsp;&nbsp;&nbsp;
[![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/clearlybaffled/homelab?style=flat-square)](https://libraries.io/github/clearlybaffled/homelab)
</div>
<br/>

Welcome to my homelab!
The repository is mostly focused on a modest kubernetes cluster with one control plane/node running all of my self hosted services and storage,
but it also serves as the Infrastructure-as-Code (IaC) for my entire home network and devices, to include: an OpnSense gateway/firewall,
a couple of workstations, wireless devices, and a Cisco switch.
Ultimately, this will include all applications for managing home IT systems.

## 🤯 Features

- [x] Kubernetes cluster deployment using kubeadm
- [x] Infrastructure Automation with Ansible to provision hosts, clusters, devices, etc.
- [x] Offline Root CA / Scripted PKI management using `openssl(1)`
- [x] Manage cluster state and apps using GitOps and ArgoCD
- [ ] FreeIPA server
- [ ] RADIUS server
- [ ] Remote access via VPN

## ⌨️ Getting Started

```console
python3 -m venv .venv
source .venv/bin/activate
pip install -U -r requirements.txt
ansible-galaxy collection install -U -r requirements.yaml
ansible-playbook homelab.yml
```

# 🍇 Cluster

## Infrastructure Automation

Host buildout is handled by [Ansible][ansible-uri] automation.
The whole lab is built out from a [top level playbook](./homelab.yml), with segment specific playbooks under the [`playbooks/`](./playbooks/) directory.
(As a convention, all Ansible yaml files are suffixed `.yml` to allow VSCode to distinguish between those and all other yaml files.)
The full task list can be found in the [infrastructure](./infrastructure/README.md) folder, but as an overview, it will:

- Install system packages and any other necessary system related setup
- Pull down cluster images and binaries
- Install container runtime and start kubelet
- Run `kubeadm` to setup to create cluster
- Creates a separate user to continue setting up the cluster with to get away from using the admin credentials
- Applies CNI configuration
- Generates Application files for every cluster app and drops them into [`cluster/bootstrap`](./cluster/bootstrap) and Kustomization files into[`cluster/apps`](./cluster/apps) for the respective apps
- Bootstraps the cluster by starting ArgoCD and then applying [`cluster/cluster.yaml`](./cluster/cluster.yaml)

## GitOps

[ArgoCD][argocd-uri] watches all subfolders under the [`cluster`](./cluster) folder (see Directories below) and makes the changes to my cluster based on the YAML manifests.

The way Argo works for me here is (almost) every file in the [`cluster/bootstrap`](./cluster/bootstrap) directory will define an `argoproj.io/v1alpha1/Application` that points to a corresponding folder under [`cluster/apps`](./cluster/apps).
The `Application` will apply any manifest files it finds in that directory,
in addition to any Helm Charts or Kustomizations [that may also be defined](https://argo-cd.readthedocs.io/en/stable/user-guide/multiple_sources/) within the `Application`'s spec.
One or more Helm `values.yaml` files are in each directory and each helm definition in the `Application` refers to the specific values file to apply to that chart.

## Directories

This Git repository contains the following top level directories.
<!-- markdownlint-disable MD013 -->
```sh
📁 cluster         # Kubernetes cluster defined in code
├─📁 apps          # Apps deployed into my cluster grouped by namespace
├─📁 argocd        # Main Argo configuration of repository
└─📁 bootstrap     # Cluster initialization flies (Argo Applications) also grouped by namespace
📁 infrastructure  # Ansible files
├─📁 inventory     # Defines Host configurations and widest scoped variables
├─📁 pki           # Self-signed CA and subordinate CA certs for whole house and cluster
├─📁 roles         # Ansible roles that define the actual steps to accomplish these tasks
└─📁 terraform     # Terraform config for building VM hosts
📁 playbooks       # Ansible playbooks
```
<!-- markdownlint-enable MD013 -->
# 🖥️ Tech Stack

## Infrastructure

|Logo|Name|Description|
|:----|:----|:--------|
|[<img width="32" src="https://simpleicons.org/icons/ansible.svg">][ansible-uri]|[Ansible](./infrastructure/)|Automate bare metal provisioning and configuration|
|[<img width="32" src="https://raw.githubusercontent.com/cncf/artwork/master/projects/argo/icon/color/argo-icon-color.svg">][argocd-uri]|[ArgoCD](./cluster/argocd/)|GitOps tool built to deploy applications to Kubernetes|
|[<img width="32" src="https://github.com/jetstack/cert-manager/raw/master/logo/logo.png">](https://cert-manager.io)|[cert-manager](./cluster/apps/infrastructure/cert-manager/)|Cloud native certificate management|
|[<img width="32" src="https://raw.github.com/cncf/artwork/master/projects/crio/icon/color/crio-icon-color.png">](https://www.cri-o.io)|[CRI-O](./infrastructure/roles/containers/runtime/)|OCI - Container Runtime|
|[<img width="32" src="https://www.debian.org/logos/openlogo-nd.svg">](https://debian.org)|Debian|Base OS for Kubernetes nodes|
|[<img width="32" src="https://raw.githubusercontent.com/flannel-io/flannel/master/logos/flannel-glyph-color.svg">](https://www.github.com/flannel-io/flannel)|[Flannel](./infrastructure/roles/containers/network/)|Kubernetes Network Plugin|
|[<img width="32" src="https://github.com/cncf/artwork/blob/master/projects/helm/icon/color/helm-icon-color.png?raw=true">](https://helm.sh)|Helm|The package manager for Kubernetes|
|[<img width="32" src="https://docs.nginx.com/nginx-ingress-controller/images/icons/NGINX-Ingress-Controller-product-icon.svg">](https://kubernetes.github.io/ingress-nginx/)|[Ingress-nginx](./cluster/apps/infrastructure/ingress-nginx/)| Ingress controller for Kubernetes using NGINX as a reverse proxy and load balancer|
|[<img width="32" src="https://www.virt-tools.org/logo-kvm.png">](https://www.linux-kvm.org)|[KVM](./infrastructure/roles/server/kvm/) | Linux Kernel Virtual Machine Hypervisor |
|[<img width="32" src="https://github.com/cncf/artwork/blob/master/projects/kubernetes/icon/color/kubernetes-icon-color.svg?raw=true">](https://kubernetes.io)|[Kubernetes](./infrastructure/roles/kubernetes/)|Container Orchestration|
|[<img width="32" src="https://libvirt.org/logos/logo-square.svg">](https://www.libvirt.org) |Libvirt| Virtualization API |
|[![](https://avatars.githubusercontent.com/u/60239468?s=32&v=4)](https://metallb.org)|[MetalLB](./cluster/apps/infrastructure/metallb/)|Bare metal load-balancer for Kubernetes|
|[<img width="32" src="https://github.com/cncf/artwork/blob/aea0dcfe090b8f36d7ae1eb3d5fbe95cc77380d3/projects/prometheus/icon/color/prometheus-icon-color.png?raw=true">](https://prometheus.io)|[Prometheus](./cluster/apps/monitoring/kube-prometheus-stack/)|Systems monitoring and alerting toolkit|
|[<img width="32" src="https://www.virt-tools.org/logo-qemu.png">](https://www.qemu.org)|QEMU|Open source machine emulator and virtualizer|
|[<img width="32" src="https://github.com/cncf/artwork/blob/master/projects/rook/icon/color/rook-icon-color.png?raw=true">](https://rook.io)|[Rook](./cluster/apps/infrastructure/rook-ceph/)|Cloud-native storage orchestrator for Ceph|
|[<img width="32" src="https://api.iconify.design/logos/terraform-icon.svg">](https://www.terraform.io/)|[Terraform](./infrastructure/terraform/)|Infrastructure provisioning automation|
|[<img width="32" src="https://docs.zerotier.com/img/ZeroTierIcon.png">](https://zerotier.com)|ZeroTier|Virtual Networking that just works|

## Applications (by namespace)

### [Database](./cluster/apps/db/)

| **Icon**|**Application**|**Category**|**Description**|**Status**|**Version**|
|--------|----------------|------------|---------------|----------|--------------------------|
|[<img width="32" src="https://www.mysql.com/common/logos/logo-mysql-170x115.png">][mysql-uri]|[MySQL](./cluster/apps/db/mysql/)| `Relational DB` | SQL Database | Deployed | [![][mysql-badge]][mysql-chart]
|[<img width="32" src="https://cloudnative-pg.io/images/hero_image.svg">][postgres-uri]| [PostgreSQL](./cluster/apps/db/cloudnative-pg/) | `Relational DB` | via [Cloudnative-PG][cnpg-uri] operator | Deployed | [![][cnpg-badge]][cnpg-chart]
|[![](https://redis.io/images/favicons/favicon-32x32.png)][redis-uri]| [Redis](./cluster/apps/db/redis/) | `Caching` | In-memory Key-Value store | Deployed | [![][redis-badge]][redis-chart]


### [Downloads](./cluster/apps/downloads/)

| **Icon**|**Application**|**Category**|**Description**|**Status**|**Version**|
|--------|----------------|------------|---------------|----------|--------------------------|
|[![](https://avatars.githubusercontent.com/u/2131270?s=32&v=4)][qbittorrent-uri]| [qBittorrent](./cluster/apps/downloads/qbittorrent/)| `Downloader` | BitTorrent client | Deployed |[![][qbittorrent-badge]][qbittorrent-img] |
|[![](https://github.com/Radarr/Radarr/blob/develop/Logo/32.png?raw=true)][radarr-uri]|[Radarr](./cluster/apps/downloads/Radarr/)| `Movies` | Movie Collection manager | Deployed |[![][radarr-badge]][radarr-img] |
|[![](https://github.com/Sonarr/Sonarr/blob/develop/Logo/32.png?raw=true)][sonarr-uri]|[Sonarr](./cluster/apps/downloads/sonarr/)| `TV` | TV Series Collection manager | Deployed |[![][sonarr-badge]][sonarr-img] |
|[![](https://github.com/Lidarr/Lidarr/blob/develop/Logo/32.png?raw=true)][lidarr-uri]|[Lidarr](./cluster/apps/downloads/lidarr/)| `Music` | Music Collection manager | Deployed | [![][lidarr-badge]][lidarr-img] |
|[![](https://github.com/Prowlarr/Prowlarr/blob/develop/Logo/32.png?raw=true)][prowlarr-uri]|[Prowlarr](./cluster/apps/downloads/prowlarr/)| `Tracker` | Tracker manager | Deployed | [![][prowlarr-badge]][prowlarr-img] |


### [Media](./cluster/apps/media/)

| **Icon**|**Application**|**Category**|**Description**|**Status**|**Version**|
|--------|----------------|------------|---------------|----------|--------------------------|
|[<img width="32" src="https://github.com/kovidgoyal/calibre/blob/master/icons/calibre.png?raw=true">][calibre-uri] | [Calibre](./cluster/apps/media/calibre/) | `Books` | E-book collection manager | Deployed | [![][calibre-badge]][calibre-img] [![][calibre-web-badge]][calibre-web-img] |

### [Services](./cluster/apps/services/)

| **Icon**|**Application**|**Category**|**Description**|**Status**|**Version**|
|--------|----------------|------------|---------------|----------|--------------------------|
|[<img width="32" src="https://raw.githubusercontent.com/grocy/grocy/master/public/img/icon.svg">][grocy-uri]| [Grocy](./cluster/apps/services/grocy/) | `Services` | ERP Beyond your fridge | Deployed | [![][grocy-badge]][grocy-img] |
|<img width="32" src="https://github.com/hay-kot/mealie/raw/mealie-next/docs/docs/assets/img/favicon.png">| [Mealie][mealie-url] | `Services` | Recipe Manager | Deployed | [![][mealie-badge]][mealie-docker] |
|<img width="32" src="https://nextcloud.com/wp-content/uploads/2022/10/nextcloud-logo-blue-transparent.svg">| [NextCloud][nextcloud-url] | `File Sharing` | File Hosting | Deployed | [![][nextcloud-badge]][nextcloud-chart] |
|<img width="32" src="https://hajimari.io/assets/logo.png">|[Hajimari][hajimari-url] | `Dashboard` | Startpage with K8S application discovery | Deployed | [![][hajimari-badge]][hajimari-url] |
|<img width="32" src="https://github.com/paperless-ngx/paperless-ngx/raw/dev/docs/assets/favicon.png">|[Paperless-ngx][paperless-uri] | `File Sharing` | Document Management System | Deployed| [![][paperless-badge]][paperless-img] |
| ![](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPHN2ZyB2aWV3Qm94PSI2Mi40MjM5IDYxLjI1MzQgNDQ5Ljg1NjQgNDQ5Ljg1NjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPGcgdHJhbnNmb3JtPSJtYXRyaXgoMSwgMCwgMCwgMSwgLTcuMTA1NDI3MzU3NjAxMDAyZS0xNSwgMCkiPgogICAgPGcgdHJhbnNmb3JtPSJtYXRyaXgoMS4xODA3NSwgMCwgMCwgMS4xODA3NSwgLTEyNjUuMzEwNDkxLCAtMTM5NS44MjAzODUpIj4KICAgICAgPGNpcmNsZSBjeD0iMTMxNC45OCIgY3k9IjE0MjQuNTIiIHI9IjE5MC40OTYiIHN0eWxlPSJmaWxsOnJnYig4OCw4NiwyMjQpOyIvPgogICAgPC9nPgogIDwvZz4KICA8ZyB0cmFuc2Zvcm09Im1hdHJpeCgxLCAwLCAwLCAxLCAtMTAxNy40OTAxMDQzMzU3NzI4LCAtMTE0MC41NTAxMDgzMTI0NDU3KSI+CiAgICA8ZyB0cmFuc2Zvcm09Im1hdHJpeCgwLjcwNzM1MSwwLjcwNjg2MiwtMC43MDY4NjIsMC43MDczNTEsMTMzMS45MywtNTEyLjgwNCkiPgogICAgICA8cGF0aCBkPSJNMTI0NC4zOSwxMjkzLjk1TDEyNDQuMzksMTQ5My41OUMxMjQ0LjM5LDE0OTMuNTkgMTI0My41OCwxNTYxLjQ4IDEzMTkuMjksMTU2Mi40N0MxMzk1LjI3LDE1NjMuNDYgMTM5NC4xNywxNDkzLjU5IDEzOTQuMTcsMTQ5My41OUwxMzk0LjE3LDEyOTMuOTUiIHN0eWxlPSJmaWxsOm5vbmU7c3Ryb2tlOndoaXRlO3N0cm9rZS13aWR0aDozMS4yNXB4OyIvPgogICAgPC9nPgogICAgPGcgdHJhbnNmb3JtPSJtYXRyaXgoLTAuNzEwMDY3LC0wLjcwNDEzNCwwLjcwNDEzNCwtMC43MTAwNjcsMTI4NC4xMiwzMzY2LjQxKSI+CiAgICAgIDxwYXRoIGQ9Ik0xMjQ0LjM5LDEyOTMuOTVMMTI0NC4zOSwxNDkzLjU5QzEyNDQuMzksMTQ5My41OSAxMjQzLjU4LDE1NjEuNDggMTMxOS4yOSwxNTYyLjQ3QzEzOTUuMjcsMTU2My40NiAxMzk0LjE3LDE0OTMuNTkgMTM5NC4xNywxNDkzLjU5TDEzOTQuMTcsMTI5My45NSIgc3R5bGU9ImZpbGw6bm9uZTtzdHJva2U6d2hpdGU7c3Ryb2tlLXdpZHRoOjMxLjI1cHg7Ii8+CiAgICA8L2c+CiAgPC9nPgo8L3N2Zz4=#Ti7xw74JX1) | [Linkding][linkding-uri] | `Bookmark Sharing`| Minimal bookmark Manager | Deployed | [![][linkding-badge]][linkding-img] | 
| <img width="32" src="https://raw.githubusercontent.com/Kovah/LinkAce/main/public/favicon.ico"> | [LinkAce][linkace-uri] | `Bookmark Sharing` | Your self-hosted bookmark archive | Deployed | [![][linkace-badge]][linkace-img] |
|<img width="32" src="https://raw.githubusercontent.com/linkwarden/linkwarden/4454e615b64f710d7104dd2042fbe97da3904f7e/public/favicon-32x32.png">|[Linkwarden][linkwarden-uri] | `Bookmark Sharing` | Collaborative Bookmark Manager | Deployed | [![][linkwarden-badge]][linkwarden-img] | 

### [Monitoring](./cluster/apps/monitoring/)

| **Icon**|**Application**|**Category**|**Description**|**Status**|**Version**|
|--------|----------------|------------|---------------|----------|--------------------------|
|[<img width="32" src="https://grafana.com/static/img/menu/grafana2.svg">][grafana-uri]|[Grafana](./cluster/apps/monitoring/kube-prometheus-stack/)| `Dashboard` | Operational dashboards | Deployed | [![][grafana-badge]][grafana-chart] |

### [Infrastructure Services](./cluster/apps/infrastructure)

| **Icon**|**Application**|**Category**|**Description**|**Status**|**Version**|
|--------|----------------|------------|---------------|----------|--------------------------|
|<img width="32" src="https://avatars.githubusercontent.com/u/44905828?s=200&v=4">|[NetBox][netbox-uri]| `Services`| Full-scale network inventory | | |
|<img width="32" src="https://simpleicons.org/icons/vault.svg">|[Vault][vault-uri]| `Services` | Secrets and encryption management| | |

### Virtualized (and other off cluster) Apps

| **Icon**|**Application**|**Category**|**Description**|**Status**|**Version**|
|--------|----------------|------------|---------------|----------|--------------------------|
|<img width="32" src="https://avatars.githubusercontent.com/u/10979201?s=200&v=4">| [FreeIPA][freeipa-uri] | `Infrastructure`| Full IdAM solution + PKI | Deploying.. | [![][freeipa-badge]][freeipa-img] |
|<img width="32" src="https://github.com/MythTV/mythtv/raw/master/mythtv/html/images/icons/upnp_small_icon.png">|[MythTV][mythtv-url]| `Media` | Digital Video Recorder | Running directly on node | [![][mythtv-badge]][mythtv-gh] |

## 🤝 Thank you

- [bjw-s/home-ops](https://github.com/bjw-s/home-ops)
- [onedr0p/home-ops](https://github.com/onedr0p/home-ops)
- [khuedoan/homelab](https://github.com/khuedoan/homelab)
- [gruberdev/homelab](https://github.com/gruberdev/homelab)
- [RickCoxDev/home-cluster](https://github.com/RickCoxDev/home-cluster)
- [billimek/k8s-gitops](https://github.com/billimek/k8s-gitops)
- [blackjid/k8s-gitops](https://github.com/blackjid/k8s-gitops)
- [carpenike/k8s-gitops](https://github.com/carpenike/k8s-gitops)
- [K8s-At-Home Project](https://k8s-at-home.com)

<details>
<summary><h3>&nbsp;📈 Repository Stats</h3></summary>
<br/>

## ⭐ Stargazers

[![Star History Chart](https://api.star-history.com/svg?repos=clearlybaffled/homelab&type=Date)](https://star-history.com/#clearlybaffled/homelab&Date)

## 🎶 Repobeats

![Alt](https://repobeats.axiom.co/api/embed/d99fddfc840ac253fd4c4975137e1561dfaf128d.svg "Repobeats analytics image")

</details>

[ansible-uri]: https://www.ansible.com
[argocd-uri]: https://argoproj.github.io

[mysql-uri]: https://www.mysql.com
[mysql-badge]: https://img.shields.io/badge/bitnami/mysql-v8.0.33-blue?logo=helm
[mysql-chart]: https://artifacthub.io/packages/helm/bitnami/mysql

[postgres-uri]: https://www.postgresql.org
[cnpg-uri]:https://cloudnative-pg.io/
[cnpg-badge]: https://img.shields.io/badge/cloudnative--pg-v1.20.0-blue?logo=helm
[cnpg-chart]: https://artifacthub.io/packages/helm/cloudnative-pg/cloudnative-pg

[redis-uri]: https://redis.io
[redis-badge]: https://img.shields.io/badge/bitnami/redis-v7.0.11-blue?logo=helm
[redis-chart]: https://artifacthub.io/packages/helm/bitnami/redis

[grocy-uri]: https://github.com/grocy/grocy
[grocy-img]: https://hub.docker.com/r/linuxserver/grocy
[grocy-badge]: https://img.shields.io/badge/linuxserver/grocy-v3.3.2-blue?logo=docker

[mealie-url]: https://mealie.io/
[mealie-badge]: https://img.shields.io/badge/mealie-v1.0.0beta5-blue?logo=docker
[mealie-docker]: https://hub.docker.com/r/hkotel/mealie

[mythtv-url]: https://www.mythtv.org
[mythtv-badge]: https://img.shields.io/badge/mythtv-v0.33-blue?logo=github
[mythtv-gh]: https://github.com/MythTV/MythTV

[nextcloud-url]: https://www.nextcloud.com
[nextcloud-badge]: https://img.shields.io/badge/nextcloud-v27.0.0-blue?logo=helm
[nextcloud-chart]: https://nextcloud.github.io/helm/

[hajimari-url]:https://hajimari.io/
[hajimari-badge]: https://img.shields.io/badge/hajimari-v2.0.2-blue?logo=helm

[grafana-badge]: https://img.shields.io/badge/grafana-v9.5.2-blue?logo=helm
[grafana-uri]: https://grafana.com
[grafana-chart]: https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack

[paperless-uri]: https://docs.paperless-ngx.com/
[paperless-badge]: https://img.shields.io/badge/paperless--ngx-v1.15.1-blue?logo=docker
[paperless-img]: https://ghcr.io/paperless-ngx/paperless-ngx

[linkding-uri]: https://github.com/sissbruecker/linkding
[linkding-badge]: https://img.shields.io/badge/linkding-1.19.1-blue?logo=docker
[linkding-img]: https://hub.docker/com/r/sissbruecker/linkding

[linkace-uri]: https://www.linkace.org/
[linkace-badge]: https://img.shields.io/badge/linkace-v1.12.2-blue?logo=docker
[linkace-img]: https://hub.docker.com/r/linkace/linkace

[linkwarden-uri]: https://linkwarden.app
[linkwarden-badge]: https://img.shields.io/badge/linkwarden-v1.2.5-blue?logo=docker
[linkwarden-img]: https://ghcr.io/linkwarden/linkwarden

[netbox-uri]: https://netbox.dev
[vault-uri]: https://www.vaultproject.io

[freeipa-uri]: https://wwww.freeipa.org
[freeipa-img]: https://quay.io/repository/freeipa/freeipa-server
[freeipa-badge]: https://img.shields.io/badge/freeipa/freeipa--server-fedora--38-blue.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNTYiIGhlaWdodD0iMjM2IiB2aWV3Qm94PSIwIDAgMjU2IDIzNiI+PHBhdGggZmlsbD0iIzQwQjRFNSIgZD0ibTIwMC4xMzQgMGw1NS41NTUgMTE3LjUxNGwtNTUuNTU1IDExNy41MThoLTQ3LjI5NWw1NS41NTUtMTE3LjUxOEwxNTIuODQgMGg0Ny4yOTVaTTExMC4wOCA5OS44MzZsMjAuMDU2LTM4LjA5MmwtMi4yOS04Ljg2OEwxMDIuODQ3IDBINTUuNTUybDQ4LjY0NyAxMDIuODk4bDUuODgxLTMuMDYyWm0xNy43NjYgNzQuNDMzbC0xNy4zMzMtMzkuMDM0bC02LjMxNC0zLjEwMWwtNDguNjQ3IDEwMi44OThoNDcuMjk1bDI1LTUyLjg4di03Ljg4M1oiLz48cGF0aCBmaWxsPSIjMDAzNzY0IiBkPSJNMTUyLjg0MiAyMzUuMDMyTDk3LjI4NyAxMTcuNTE0TDE1Mi44NDIgMGg0Ny4yOTVsLTU1LjU1NSAxMTcuNTE0bDU1LjU1NSAxMTcuNTE4aC00Ny4yOTVabS05Ny4yODcgMEwwIDExNy41MTRMNTUuNTU1IDBoNDcuMjk2TDQ3LjI5NSAxMTcuNTE0bDU1LjU1NiAxMTcuNTE4SDU1LjU1NVoiLz48L3N2Zz4=

[qbittorrent-uri]: https://www.qbittorrent.org/
[qbittorrent-img]: https://ghcr.io/onedr0p/qbittorrent
[qbittorrent-badge]: https://img.shields.io/badge/onedr0p/qbittorrent-4.6.0-blue?logo=docker


[lidarr-uri]: https://lidarr.audio
[lidarr-img]: https://ghcr.io/onedr0p/lidarr
[lidarr-badge]: https://img.shields.io/badge/onedr0p/lidarr-1.4.5-blue?logo=docker

[radarr-uri]: https://radarr.video
[radarr-img]: https://ghcr.io/onedr0p/radarr
[radarr-badge]: https://img.shields.io/badge/onedr0p/radarr-5.0.3.8127-blue?logo=docker

[sonarr-uri]: https://sonarr.tv
[sonarr-img]: https://ghcr.io/onedr0p/sonarr
[sonarr-badge]: https://img.shields.io/badge/onedr0p/sonarr--develop-4.0.0.710-blue?logo=docker

[prowlarr-uri]: https://github.com/Prowlarr/Prowlarr
[prowlarr-img]: https://ghcr.io/onedr0p/prowlarr
[prowlarr-badge]: https://img.shields.io/badge/onedr0p/prowlarr-1.9.4-blue?logo=docker

[calibre-uri]: https://calibre-ebook.com/
[calibre-img]: https://ghcr.io/linuxserver/calibre
[calibre-web-img]: https://ghcr.io/linuxserver/calibre-web
[calibre-badge]:https://img.shields.io/badge/linuxserver/calibre-version--v6.29.0-blue?logo=docker
[calibre-web-badge]: https://img.shields.io/badge/linuxserver/calibre--web-version--0.6.21-blue?logo=docker