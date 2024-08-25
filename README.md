<!-- markdownlint-disable-next-line MD013 -->
<h1 tabindex="-1" dir="auto" style="bottom-border:none;"><img src="https://camo.githubusercontent.com/0b88a728a74d44cb11f842cbed1cacb61f4d67f09b3dcf5926ac4767a1bb1c27/68747470733a2f2f692e696d6775722e636f6d2f7031527a586a512e706e67" width="144px" height="144px" align="left"/>

<!-- markdownlint-disable-next-line MD013 -->
<a id="user-content-homelab" class="anchor" aria-hidden="true" href="#homelab"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a>
Homelab
</h1>

> K8S cluster built with Ansible and managed using ArgoCD for GitOps

<div align="center">

[![Discord](https://img.shields.io/badge/discord-chat-7289DA.svg?maxAge=60&style=flat-square&logo=discord)](https://discord.gg/DNCynrJ)&nbsp;&nbsp;&nbsp;
[![k8s](https://img.shields.io/badge/k8s-v1.29.2-blue?style=flat-square&logo=kubernetes)](https://k8s.io/)&nbsp;&nbsp;&nbsp;
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
- [x] FreeIPA server
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
|[<img width="32" src="https://simpleicons.org/icons/ansible.svg">][ansible-uri] | [Ansible](./infrastructure/) | Automate bare metal provisioning and configuration|
|[<img width="32" src="https://raw.githubusercontent.com/cncf/artwork/master/projects/argo/icon/color/argo-icon-color.svg">][argocd-uri] | [ArgoCD](./cluster/argocd/) | GitOps tool built to deploy applications to Kubernetes|
|[<img width="32" src="https://github.com/jetstack/cert-manager/raw/master/logo/logo.png">](https://cert-manager.io) | [cert-manager](./cluster/apps/infrastructure/cert-manager/) | Cloud native certificate management|
|[<img width="32" src="https://raw.github.com/cncf/artwork/master/projects/crio/icon/color/crio-icon-color.png">](https://www.cri-o.io) | [CRI-O](./infrastructure/roles/containers/runtime/) | OCI - Container Runtime|
|[<img width="32" src="https://www.debian.org/logos/openlogo-nd.svg">](https://debian.org) | Debian | Base OS for Kubernetes nodes|
|[<img width="32" src="https://github.com/kubernetes-sigs/external-dns/raw/master/docs/img/external-dns.png">](https://github.com/kubernetes-sigs/external-dns) | [External DNS](./cluster/apps/infrastructure/external-dns/) | Synchronize exposed services and ingresses with DNS providers |
|[<img width="32" src="https://raw.githubusercontent.com/flannel-io/flannel/master/logos/flannel-glyph-color.svg">](https://www.github.com/flannel-io/flannel) | [Flannel](./infrastructure/roles/containers/network/) | Kubernetes Network Plugin|
|[<img width="32" src="https://raw.githubusercontent.com/cncf/artwork/main/projects/helm/icon/color/helm-icon-color.png">](https://helm.sh) | Helm | The package manager for Kubernetes|
|[<img width="32" src="https://docs.nginx.com/nginx-ingress-controller/images/icons/NGINX-Ingress-Controller-product-icon.svg">](https://kubernetes.github.io/ingress-nginx/) | [Ingress-nginx](./cluster/apps/infrastructure/ingress-nginx/)| Ingress controller for Kubernetes using NGINX as a reverse proxy and load balancer|
|[<img width="32" src="https://kubernetes.io/images/kubeadm-stacked-color.png">](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/) | [kubeadm](./infrastructure/roles/kubernetes/control_plane/)| Official command-line cluster management tool |
|[<img width="32" src="https://www.virt-tools.org/logo-kvm.png">](https://www.linux-kvm.org) | [KVM](./infrastructure/roles/server/kvm/) | Linux Kernel Virtual Machine Hypervisor |
|[<img width="32" src="https://raw.githubusercontent.com/cncf/artwork/main/projects/kubernetes/icon/color/kubernetes-icon-color.svg">](https://kubernetes.io) | [Kubernetes](./infrastructure/roles/kubernetes/) | Container Orchestration|
|[<img width="32" src="https://libvirt.org/logos/logo-square.svg">](https://www.libvirt.org) |Libvirt| Virtualization API |
|[![](https://avatars.githubusercontent.com/u/60239468?s=32&v=4)](https://metallb.org) | [MetalLB](./cluster/apps/infrastructure/metallb/) | Bare metal load-balancer for Kubernetes|
|[<img width="32" src="https://github.com/oauth2-proxy/oauth2-proxy/raw/master/docs/static/img/logos/OAuth2_Proxy_icon.svg">](https://oauth2-proxy.github.io/) | [OAuth2 Proxy](./cluster/apps/infrastructure/oauth2-proxy/) | Forward Auth for OpenID Connect|
|[<img width="32" src="https://github.com/cncf/artwork/blob/aea0dcfe090b8f36d7ae1eb3d5fbe95cc77380d3/projects/prometheus/icon/color/prometheus-icon-color.png?raw=true">](https://prometheus.io) | [Prometheus](./cluster/apps/monitoring/kube-prometheus-stack/) | Systems monitoring and alerting toolkit|
|[<img width="32" src="https://www.virt-tools.org/logo-qemu.png">](https://www.qemu.org) | QEMU | Open source machine emulator and virtualizer|
|[<img width="32" src="https://api.iconify.design/logos/terraform-icon.svg">](https://www.terraform.io/) | [Terraform](./infrastructure/terraform/) | Infrastructure provisioning automation|
|[<img width="32" src="https://docs.zerotier.com/img/ZeroTierIcon.png">](https://zerotier.com) | ZeroTier | Virtual Networking that just works|

## Applications (by namespace)

### [Homepage](./cluster/apps/services/homepage/)

| **Icon**|**Application**|**Category**|**Description**|**Status**|**Version**|
|--------|----------------|------------|---------------|----------|--------------------------|
|[<img width="32" src="https://raw.githubusercontent.com/gethomepage/homepage/main/docs/assets/favicon.ico">][homepage-uri] | [Homepage](./cluster/apps/services/homepage)| `Home` | Landing page for exploring the cluster, with live widgets! | Deployed | [![][homepage-badge]][homepage-chart] |

### [Database](./cluster/apps/db/)

| **Icon**|**Application**|**Category**|**Description**|**Status**|**Version**|
|--------|----------------|------------|---------------|----------|--------------------------|
|[<img width="32" src="https://www.mysql.com/common/logos/logo-mysql-170x115.png">][mysql-uri] | [MySQL](./cluster/apps/db/mysql/)| `Relational DB` | SQL Database | Deployed | [![][mysql-badge]][mysql-chart] |
|[<img width="32" src="https://cloudnative-pg.io/images/hero_image.svg">][postgres-uri]| [PostgreSQL](./cluster/apps/db/cloudnative-pg/) | `Relational DB` | via [Cloudnative-PG][cnpg-uri] operator | Deployed | [![][cnpg-badge]][cnpg-chart] |
|[![](https://raw.githubusercontent.com/redis/docs/main/static/images/icon-redis.svg)][redis-uri]| [Redis](./cluster/apps/db/redis/) | `Caching` | In-memory Key-Value store | Deployed | [![][redis-badge]][redis-chart] |

### [Downloads](./cluster/apps/downloads/)

| **Icon**|**Application**|**Category**|**Description**|**Status**|**Version**|
|--------|----------------|------------|---------------|----------|--------------------------|
|[![](https://avatars.githubusercontent.com/u/2131270?s=32&v=4)][qbittorrent-uri]| [qBittorrent](./cluster/apps/downloads/qbittorrent/)| `Downloader` | BitTorrent client | Deployed |[![][qbittorrent-badge]][qbittorrent-img] |
|[![](https://github.com/Radarr/Radarr/blob/develop/Logo/32.png?raw=true)][radarr-uri] | [Radarr](./cluster/apps/downloads/radarr/)| `Movies` | Movie Collection manager | Deployed |[![][radarr-badge]][radarr-img] |
|[![](https://github.com/Sonarr/Sonarr/blob/develop/Logo/32.png?raw=true)][sonarr-uri] | [Sonarr](./cluster/apps/downloads/sonarr/)| `TV` | TV Series Collection manager | Deployed |[![][sonarr-badge]][sonarr-img] |
|[![](https://github.com/Lidarr/Lidarr/blob/develop/Logo/32.png?raw=true)][lidarr-uri] | [Lidarr](./cluster/apps/downloads/lidarr/)| `Music` | Music Collection manager | Deployed | [![][lidarr-badge]][lidarr-img] |
|[![](https://github.com/Readarr/Readarr/blob/develop/Logo/32.png?raw=true)][readarr-uri] | [Readarr](./cluster/apps/downloads/readarr/)| `Ebooks` | Ebook and audiobook collection manager | Deployed | [![][readarr-badge]][readarr-img] |
|[![](https://github.com/Prowlarr/Prowlarr/blob/develop/Logo/32.png?raw=true)][prowlarr-uri] | [Prowlarr](./cluster/apps/downloads/prowlarr/)| `Tracker` | Tracker manager | Deployed | [![][prowlarr-badge]][prowlarr-img] |
|[<img width="32" src="https://raw.githubusercontent.com/bazarr/wiki/main/docs/img/logo.png">][bazarr-uri] | [Bazarr](./cluster/apps/downloads/bazarr/)| `Subtitles` | Subtitle download manager | | [![][bazarr-badge]][bazarr-img] |

### [Home](./cluster/apps/home)

| **Icon**|**Application**|**Category**|**Description**|**Status**|**Version**|
|--------|----------------|------------|---------------|----------|--------------------------|
|[<img width="32" src="https://raw.githubusercontent.com/grocy/grocy/master/public/img/icon.svg">][grocy-uri] | [Grocy](./cluster/apps/home/grocy/) | `Services` | ERP Beyond your fridge | Deployed | [![][grocy-badge]][grocy-img] |
|[<img width="32" src="https://github.com/hay-kot/mealie/raw/mealie-next/docs/docs/assets/img/favicon.png">][mealie-url] | [Mealie](./cluster/apps/home/mealie/) | `Services` | Recipe Manager | Deployed | [![][mealie-badge]][mealie-docker] |
|[<img width="32" src="https://github.com/paperless-ngx/paperless-ngx/raw/dev/docs/assets/favicon.png">][paperless-uri] |[Paperless-ngx](./cluster/apps/home/paperless-ngx/) | `File Sharing` | Document Management System | Deployed| [![][paperless-badge]][paperless-img] [![][node-hp-scan-to-badge]][node-hp-scan-to-img] |
|[<img width="32" src="https://brands.home-assistant.io/homeassistant/icon.png">][home-assistant-uri] | [Home Assistant](./cluster/apps/home/home-assistant/) | `Home Automation` | Open source home automation | Deployed | [![Home Assistant][home-assistant-badge]][home-assistant-img] [![Code Server][code-server-badge]][code-server-img] |
|[<img width="32" src="https://hay-kot.github.io/homebox/assets/img/favicon.svg">][homebox-uri] | [Homebox](./cluster/apps/home/homebox/) | `Home inventory` | Inventory and organization for the Home User | Deployed | [![Homebox][homebox-badge]][homebox-img] |
|[<img width="32" src="https://raw.githubusercontent.com/eclipse/mosquitto/master/logo/mosquitto-logo-min.svg">][mosquitto-uri] | [Mosquitto](./cluster/apps/home/mosquitto) | `MQTT Broker` | Eclipse-foundation MQTT broker implementation | Deployed | [![Mosquitto][mosquitto-badge]][mosquitto-img] |
|[<img width="32" src="https://avatars.githubusercontent.com/u/6574523?s=200&v=4">][owntracks-uri] | [Owntracks](./cluster/apps/home/owntracks) | `Location Tracking` | Keep track of your own location | Deployed | [![owntracks-badge]][owntracks-img] [![owntracks-fe-badge]][owntracks-fe-img] |
|[<img width="32" src="https://raw.githubusercontent.com/blakeblackshear/frigate/dev/docs/static/img/logo.svg">][frigate-uri] | [Frigate NVR](./cluster/apps/home/nvr) | `NVR` | Home video monitoring | In Progress | [![Frigate][frigate-badge]][frigate-chart] [![Wyze-Bridge][wyze-bridge-badge]][wyze-bridge-img] |
|[<img width="32" src="https://raw.githubusercontent.com/zwave-js/zwave-js-ui/master/public/logo.svg">][zwave-js-uri] | [Z-Wave JS](./cluster/apps/home/zwave-js-ui) | `Z-Wave Controller` | Z-Wave Controller written in javascript | Deployed | [![zwave-js=badge]][zwave-js-img] |

### [Infrastructure Services](./cluster/apps/infrastructure)

| **Icon**|**Application**|**Category**|**Description**|**Status**|**Version**|
|--------|----------------|------------|---------------|----------|--------------------------|
|[<img width="32" src="https://raw.githubusercontent.com/netbox-community/netbox/develop/netbox/project-static/img/netbox_icon.svg">][netbox-uri] | [NetBox](./cluster/apps/infrastructure/netbox/)| `Inventory`| Full-scale network inventory | Deployed | [![netbox-badge]][netbox-chart] |
|[<img width="32" src="https://raw.githubusercontent.com/keycloak/keycloak/main/js/apps/admin-ui/public/icon.svg">][keycloak-url] | [Keycloak](./cluster/apps/infrastructure/keycloak)| `SSO` | Identity and Access Management solution | Deployed | [![keycloak-badge]][keycloak-operator] |
|[<img width="32" src="https://avatars.githubusercontent.com/u/99263827?s=32&v=4">][kubeshark-uri] | [Kubeshark](./cluster/apps/infrastructure/kubeshark/) | `Network traffic` | API traffic analyzer for Kubernetes | | [![][kubeshark-badge]][kubeshark-chart] |
|[<img width="32" src="https://github.com/stakater/Reloader/blob/master/assets/web/reloader-round-100px.png?raw=true">][reloader-uri]| [Reloader](./cluster/apps/infrastructure/reloader/) | `Configuration Management` | Controller for rolling upgrades when ConfigMaps or Secret s hange | Deployed | [![][reloader-badge]][reloader-chart] |
|[<img width="32" src="https://simpleicons.org/icons/vault.svg">][vault-uri] | Vault| `Services` | Secrets and encryption management| | |

### [Media](./cluster/apps/media/)

| **Icon**|**Application**|**Category**|**Description**|**Status**|**Version**|
|--------|----------------|------------|---------------|----------|--------------------------|
|[<img width="32" src="https://github.com/kovidgoyal/calibre/blob/master/icons/calibre.png?raw=true">][calibre-uri] | [Calibre](./cluster/apps/media/calibre/) | `Books` | E-book collection manager | Deployed | [![][calibre-badge]][calibre-img] [![][calibre-web-badge]][calibre-web-img] |
|[<img width="32" src="https://raw.githubusercontent.com/advplyr/audiobookshelf/84160b2f07164605295d6cb6f7f7925cbdf538e4/client/static/icon.svg">][audiobookshelf-uri]| [Audiobookshelf](./cluster/apps/media/audiobookshelf) | `Audio Books` | Self-hosted audiobook and podcast server | Deployed | [![][audiobookshelf-badge]][audiobookshelf-img] |
|[<img width="32" src="https://raw.githubusercontent.com/jellyfin/jellyfin-web/master/src/assets/img/icon-transparent.png">][jellyfin-uri] | [Jellyfin](./cluster/apps/media/jellyfin/) | `Media Server` | The open source media server | Deployed | [![][jellyfin-badge]][jellyfin-img] [![Jellyseer][jellyseer-badge]][jellyseer-img] |
|[<img width="32" src="https://raw.githubusercontent.com/immich-app/immich/main/design/immich-logo.png">][immich-uri] | [Immich](./cluster/apps/media/immich/)| `Photos` | Photo Management | Deployed | [![][immich-badge]][immich-chart] |
|[<img width="32" src="https://github.com/metabrainz/design-system/raw/master/brand/logos/ListenBrainz/SVG/ListenBrainz_logo_no_text.svg">][listenbrainz-uri] | ListenBrainz| `Scrobble` | Open Source scrobbler | Planned | |
|[<img src="https://raw.githubusercontent.com/photoprism/photoprism/develop/assets/static/icons/logo/32.png">][photoprism-uri] | [Photoprism](./cluster/apps/media/photoprism/)| `Photos` | Photo Management | Deployed | [![][photoprism-badge]][photoprism-img]  |
|[<img width="32" src="https://raw.githubusercontent.com/navidrome/navidrome/master/resources/logo-192x192.png">][navidrome-uri] | [Navidrome](./cluster/apps/media/navidrome/) | `Music Streaming` | Your Personal Streaming Service | Deployed | [![][navidrome-badge]][navidrome-img] |

### [Services](./cluster/apps/services/)

| **Icon**|**Application**|**Category**|**Description**|**Status**|**Version**|
|--------|----------------|------------|---------------|----------|--------------------------|
|[<img width="32" src="https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/changedetection-io.png">][changedetection-io-url] | [Change Detection](./cluster/apps/services/change-detection/) | `Website Monitoring` | Website Change Detection ... For Clever People | Deployed | [![changedetection-io-badge]][changedetection-io-img] |
| [![](./cluster/apps/services/linkding/linkding.svg)][linkding-uri]  | [Linkding](./cluster/apps/services/linkding/) | `Bookmark Sharing`| Minimal bookmark Manager | Deployed | [![][linkding-badge]][linkding-img] |
|[<img width="32" src="https://raw.githubusercontent.com/Kovah/LinkAce/main/public/favicon.ico">][linkace-uri] | [LinkAce](./cluster/apps/services/linkace/) | `Bookmark Sharing` | Your self-hosted bookmark archive | Deployed | [![][linkace-badge]][linkace-img] |
|[<img width="32" src="https://raw.githubusercontent.com/linkwarden/linkwarden/4454e615b64f710d7104dd2042fbe97da3904f7e/public/favicon-32x32.png">][linkwarden-uri] |[Linkwarden](./cluster/apps/services/linkwarden/) | `Bookmark Sharing` | Collaborative Bookmark Manager | Deployed | [![][linkwarden-badge]][linkwarden-img] |
|[<img width="32" src="https://raw.githubusercontent.com/Stirling-Tools/Stirling-PDF/main/docs/stirling.png">][stirling-pdf-uri] | [Stirling PDF](./cluster/apps/services/stirling-pdf/) | `Document Editing` | Self-hosted PDF editor | Deployed | [![][stirling-pdf-badge]][stirling-pdf-img] |
|[<img width="32" src="https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/wallabag.svg">][wallabag-uri] | [Wallabag](./cluster/apps/services/wallabag) | `Article Saver` | Save and classify articles. Read them later. Freely. | Deployed | [![][wallabag-badge]][wallabag-img] |
|[<img width="32" src="https://raw.githubusercontent.com/wger-project/wger/master/wger/core/static/images/logos/logo.png">][wger-uri] | [Wger](./cluster/apps/services/wger/) | `Health tracking` | Workout and food tracker | Broken| [![][wger-badge]][wger-img] |

### [Monitoring](./cluster/apps/monitoring/)

| **Icon**|**Application**|**Category**|**Description**|**Status**|**Version**|
|--------|----------------|------------|---------------|----------|--------------------------|
|[<img width="32" src="https://grafana.com/static/img/menu/grafana2.svg">][grafana-uri] | [Grafana](./cluster/apps/monitoring/kube-prometheus-stack/)| `Dashboard` | Operational dashboards | Deployed | [![][grafana-badge]][grafana-chart] |

### Virtualized (and other off cluster) Apps

| **Icon**|**Application**|**Category**|**Description**|**Status**|**Version**|
|--------|----------------|------------|---------------|----------|--------------------------|
|<img width="32" src="https://avatars.githubusercontent.com/u/10979201?s=200&v=4">| [FreeIPA][freeipa-uri] | `Infrastructure`| Full IdAM solution + PKI | Deployed | [![][freeipa-badge]][freeipa-img] |
|<img width="32" src="https://github.com/MythTV/mythtv/raw/master/mythtv/html/images/icons/upnp_small_icon.png"> | [MythTV][mythtv-url]| `Media` | Digital Video Recorder | Running directly on node | [![][mythtv-badge]][mythtv-gh] |

# 🤝 Thank you

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
[mysql-badge]: https://img.shields.io/badge/bitnami/mysql-v9.14.3-blue?logo=helm
[mysql-chart]: https://artifacthub.io/packages/helm/bitnami/mysql

[postgres-uri]: https://www.postgresql.org
[cnpg-uri]:https://cloudnative-pg.io/
[cnpg-badge]: https://img.shields.io/badge/cloudnative--pg-v1.22.1-blue?logo=helm
[cnpg-chart]: https://artifacthub.io/packages/helm/cloudnative-pg/cloudnative-pg

[redis-uri]: https://redis.io
[redis-badge]: https://img.shields.io/badge/bitnami/redis-v18.19.2-blue?logo=helm
[redis-chart]: https://artifacthub.io/packages/helm/bitnami/redis

[grocy-uri]: https://github.com/grocy/grocy
[grocy-img]: https://hub.docker.com/r/grocy/frontend
[grocy-badge]: https://img.shields.io/badge/grocy/grocy-v4.2.0-blue?logo=docker

[mealie-url]: https://mealie.io/
[mealie-badge]: https://img.shields.io/badge/mealie-v1.11.0-blue?logo=docker
[mealie-docker]: https://ghcr.io/mealie-recipes/mealie

[mythtv-url]: https://www.mythtv.org
[mythtv-badge]: https://img.shields.io/badge/mythtv-v0.33-blue?logo=github
[mythtv-gh]: https://github.com/MythTV/MythTV

[homepage-uri]: https://gethomepage.dev/
[homepage-badge]: https://img.shields.io/badge/jameswynn/homepage-v1.2.3-blue?logo=helm
[homepage-chart]: https://jameswynn.github.io/helm-charts/

[grafana-badge]: https://img.shields.io/badge/grafana-v9.5.2-blue?logo=helm
[grafana-uri]: https://grafana.com
[grafana-chart]: https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack

[paperless-uri]: https://docs.paperless-ngx.com/
[paperless-badge]: https://img.shields.io/badge/paperless--ngx-v2.8.6-blue?logo=docker
[paperless-img]: https://ghcr.io/paperless-ngx/paperless-ngx
[node-hp-scan-to-badge]: https://img.shields.io/badge/manuc66/node--hp--scan--to-v1.4.3-blue?logo=docker
[node-hp-scan-to-img]: https://hub.docker.com/r/manuc66/node-hp-scan-to

[linkding-uri]: https://github.com/sissbruecker/linkding
[linkding-badge]: https://img.shields.io/badge/linkding-1.19.1-blue?logo=docker
[linkding-img]: https://hub.docker/com/r/sissbruecker/linkding

[linkace-uri]: https://www.linkace.org/
[linkace-badge]: https://img.shields.io/badge/linkace-v1.12.2-blue?logo=docker
[linkace-img]: https://hub.docker.com/r/linkace/linkace

[linkwarden-uri]: https://linkwarden.app
[linkwarden-badge]: https://img.shields.io/badge/linkwarden-v2.4.8-blue?logo=docker
[linkwarden-img]: https://ghcr.io/linkwarden/linkwarden

[netbox-uri]: https://netbox.dev
[netbox-chart]: https://artifacthub.io/packages/helm/bootc/netbox
[netbox-badge]: https://img.shields.io/badge/bootc/netbox-4.1.1-blue?logo=helm
[vault-uri]: https://www.vaultproject.io

[freeipa-uri]: https://wwww.freeipa.org
[freeipa-img]: https://quay.io/repository/freeipa/freeipa-server
[freeipa-badge]: https://img.shields.io/badge/freeipa--server-fedora--38-blue.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNTYiIGhlaWdodD0iMjM2IiB2aWV3Qm94PSIwIDAgMjU2IDIzNiI+PHBhdGggZmlsbD0iIzQwQjRFNSIgZD0ibTIwMC4xMzQgMGw1NS41NTUgMTE3LjUxNGwtNTUuNTU1IDExNy41MThoLTQ3LjI5NWw1NS41NTUtMTE3LjUxOEwxNTIuODQgMGg0Ny4yOTVaTTExMC4wOCA5OS44MzZsMjAuMDU2LTM4LjA5MmwtMi4yOS04Ljg2OEwxMDIuODQ3IDBINTUuNTUybDQ4LjY0NyAxMDIuODk4bDUuODgxLTMuMDYyWm0xNy43NjYgNzQuNDMzbC0xNy4zMzMtMzkuMDM0bC02LjMxNC0zLjEwMWwtNDguNjQ3IDEwMi44OThoNDcuMjk1bDI1LTUyLjg4di03Ljg4M1oiLz48cGF0aCBmaWxsPSIjMDAzNzY0IiBkPSJNMTUyLjg0MiAyMzUuMDMyTDk3LjI4NyAxMTcuNTE0TDE1Mi44NDIgMGg0Ny4yOTVsLTU1LjU1NSAxMTcuNTE0bDU1LjU1NSAxMTcuNTE4aC00Ny4yOTVabS05Ny4yODcgMEwwIDExNy41MTRMNTUuNTU1IDBoNDcuMjk2TDQ3LjI5NSAxMTcuNTE0bDU1LjU1NiAxMTcuNTE4SDU1LjU1NVoiLz48L3N2Zz4=

[qbittorrent-uri]: https://www.qbittorrent.org/
[qbittorrent-img]: https://ghcr.io/onedr0p/qbittorrent
[qbittorrent-badge]: https://img.shields.io/badge/onedr0p/qbittorrent-4.6.6-blue?logo=docker

[lidarr-uri]: https://lidarr.audio
[lidarr-img]: https://ghcr.io/onedr0p/lidarr
[lidarr-badge]: https://img.shields.io/badge/onedr0p/lidarr-2.3.3-blue?logo=docker

[radarr-uri]: https://radarr.video
[radarr-img]: https://ghcr.io/onedr0p/radarr
[radarr-badge]: https://img.shields.io/badge/onedr0p/radarr-5.6.0-blue?logo=docker

[sonarr-uri]: https://sonarr.tv
[sonarr-img]: https://ghcr.io/onedr0p/sonarr
[sonarr-badge]: https://img.shields.io/badge/onedr0p/sonarr--develop-4.0.5-blue?logo=docker

[prowlarr-uri]: https://github.com/Prowlarr/Prowlarr
[prowlarr-img]: https://ghcr.io/onedr0p/prowlarr
[prowlarr-badge]: https://img.shields.io/badge/onedr0p/prowlarr-1.18.0-blue?logo=docker

[readarr-uri]: https://readarr.com
[readarr-img]: https://ghcr.io/onedr0p/readarr-develop
[readarr-badge]: https://img.shields.io/badge/onedr0p/readarr--develop-0.3.27-blue?logo=docker

[bazarr-uri]: https://www.bazarr.media/
[bazarr-img]: https://ghcr.io/onedr0p/bazarr
[bazarr-badge]: https://img.shields.io/badge/onedr0p/bazarr-1.4.2-blue?logo=docker

[calibre-uri]: https://calibre-ebook.com/
[calibre-img]: https://ghcr.io/linuxserver/calibre
[calibre-web-img]: https://ghcr.io/linuxserver/calibre-web
[calibre-badge]:https://img.shields.io/badge/calibre-version--v7.15.0-blue?logo=linuxserver
[calibre-web-badge]: https://img.shields.io/badge/calibre--web-version--0.6.22-blue?logo=linuxserver

[audiobookshelf-uri]: https://www.audiobookshelf.org/
[audiobookshelf-img]: https://ghcr.io/advplyr/audiobookshelf
[audiobookshelf-badge]: https://img.shields.io/badge/advplyr/audiobookshelf-2.10.1-blue?logo=docker

[jellyfin-uri]: https://jellyfin.org
[jellyfin-img]: https://hub.docker.com/r/jellyfin/jellyfin
[jellyfin-badge]: https://img.shields.io/badge/jellyfin/jellyfin-10.9.4-blue?logo=docker
[jellyseer-img]: https://hub.docker.com/r/fallenbagel/jellyseerr
[jellyseer-badge]: https://img.shields.io/badge/fallenbagel/jellyseer-1.9.0-blue?logo=docker

[immich-uri]: https://immich.app
[immich-chart]: https://immich-app.github.io/immich-charts
[immich-badge]: https://img.shields.io/badge/immich-v1.108.0-blue?logo=docker

[photoprism-uri]: https://www.photoprism.app/
[photoprism-badge]: https://img.shields.io/badge/photoprism-240711-blue?logo=docker
[photoprism-img]: https://hub.docker.com/r/photoprism/photoprism

[navidrome-uri]: https://www.navidrome.org/
[navidrome-badge]: https://img.shields.io/badge/navidrome-0.52.5-blue?logo=docker
[navidrome-img]: https://ghcr.io/navidrome/navidrome

[stirling-pdf-uri]: https://stirlingtools.com/
[stirling-pdf-badge]: https://img.shields.io/badge/frooodle/s--pdf-0.27.0-blue?logo=docker
[stirling-pdf-img]: https://hub.docker.com/r/frooodle/s-pdf

[home-assistant-uri]: https://www.home-assistant.io/
[home-assistant-badge]: https://img.shields.io/badge/home--assistant-2024.8.0-blue?logo=docker
[home-assistant-img]: https://ghcr.io/home-assistant/home-assistant
[code-server-badge]: https://img.shields.io/badge/coder/code--server-4.91.1-blue?logo=docker
[code-server-img]: https://ghcr.io/coder/code-server

[homebox-uri]: https://hay-kot.github.io/homebox/
[homebox-badge]: https://img.shields.io/badge/hay--kot/homebox-0.13.2-blue?logo=docker
[homebox-img]: https://ghcr.io/hay-kot/homebox

[wger-uri]: https://wger.de/en/software/features
[wger-badge]: https://img.shields.io/badge/wger/server-2.3--dev-blue?logo=docker
[wger-img]: https://hub.docker.com/r/wger/server

[kubeshark-uri]: https://www.kubeshark.co/
[kubeshark-badge]: https://img.shields.io/badge/kubeshark-52.1.9-blue?logo=helm
[kubeshark-chart]: https://artifacthub.io/packages/helm/kubeshark-helm-charts/kubeshark

[listenbrainz-uri]: https://listenbrainz.org

[frigate-uri]: https://frigate.video/
[frigate-badge]: https://img.shields.io/badge/blakeblackshear/frigate-7.5.1-blue?logo=helm
[frigate-chart]: https://github.com/blakeblackshear/blakeshome-charts/tree/master/charts/frigate
[wyze-bridge-badge]: https://img.shields.io/badge/mrtl8/wyze--bridge-2.9.4-blue?logo=docker
[wyze-bridge-img]: https://hub.docker.com/r/mrlt8/wyze-bridge

[mosquitto-uri]: https://mosquitto.org/
[mosquitto-img]: https://public.ecr.aws/docker/library/eclipse-mosquitto
[mosquitto-badge]: https://img.shields.io/badge/eclipse--mosquitto-2.0.18-blue?logo=docker

[changedetection-io-url]: https://changedetection.io/
[changedetection-io-img]: https://ghcr.io/dgtlmoon/changedetection.io
[changedetection-io-badge]: https://img.shields.io/badge/dgtlmoon/changedetection.io-0.45.26-blue?logo=docker

[reloader-uri]: https://github.com/stakater/Reloader
[reloader-badge]: https://img.shields.io/badge/stakater/reloader-1.0.69-blue?logo=helm
[reloader-chart]: https://stakater.github.io/stakater-charts

[owntracks-uri]: https://owntracks.org/
[owntracks-badge]: https://img.shields.io/badge/owntracks/recoeder-0.9.8--39-blue?logo=docker
[owntracks-img]: https://hub.docker.com/r/owntracks/recorder
[owntracks-fe-badge]: https://img.shields.io/badge/owntracks/frontend-2.15.3-blue?logo=docker
[owntracks-fe-img]: https://hub.docker.com/r/owntracks/frontend

[wallabag-uri]: https://wallabag.org/
[wallabag-badge]: https://img.shields.io/badge/wallabag-2.6.9-blue?logo=docker
[wallabag-img]: https://hub.docker.com/r/wallabag/wallabag

[zwave-js-uri]: https://github.com/zwave-js/zwave-js-ui
[zwave-js=badge]: https://img.shields.io/badge/zwave--js/zwave--js--ui-9.14.6-blue?logo=docker
[zwave-js-img]: https://ghcr.io/zwave-jq/zwave-js-ui

[keycloak-url]: https://www.keycloak.org/
[keycloak-operator]: https://operatorhub.io/operator/keycloak-operator
[keycloak-badge]: https://img.shields.io/badge/keycloak-25.0.2-blue.svg?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPHN2ZyB2aWV3Qm94PSIwIDMwLjgwMDUgNDkwLjYgNDM2LjkiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPGcgZmlsbD0iIzYxREFGQiIgdHJhbnNmb3JtPSJtYXRyaXgoMC45OTk5OTk5OTk5OTk5OTk5LCAwLCAwLCAwLjk5OTk5OTk5OTk5OTk5OTksIC0xNzUuNzAwMDk3NjY0NDUwMjUsIC00Ny4xOTk0OTU4Njk4NDg1MjYpIj4KICAgIDxwYXRoIGQ9Ik02NjYuMyAyOTYuNWMwLTMyLjUtNDAuNy02My4zLTEwMy4xLTgyLjQgMTQuNC02My42IDgtMTE0LjItMjAuMi0xMzAuNC02LjUtMy44LTE0LjEtNS42LTIyLjQtNS42djIyLjNjNC42IDAgOC4zLjkgMTEuNCAyLjYgMTMuNiA3LjggMTkuNSAzNy41IDE0LjkgNzUuNy0xLjEgOS40LTIuOSAxOS4zLTUuMSAyOS40LTE5LjYtNC44LTQxLTguNS02My41LTEwLjktMTMuNS0xOC41LTI3LjUtMzUuMy00MS42LTUwIDMyLjYtMzAuMyA2My4yLTQ2LjkgODQtNDYuOVY3OGMtMjcuNSAwLTYzLjUgMTkuNi05OS45IDUzLjYtMzYuNC0zMy44LTcyLjQtNTMuMi05OS45LTUzLjJ2MjIuM2MyMC43IDAgNTEuNCAxNi41IDg0IDQ2LjYtMTQgMTQuNy0yOCAzMS40LTQxLjMgNDkuOS0yMi42IDIuNC00NCA2LjEtNjMuNiAxMS0yLjMtMTAtNC0xOS43LTUuMi0yOS00LjctMzguMiAxLjEtNjcuOSAxNC42LTc1LjggMy0xLjggNi45LTIuNiAxMS41LTIuNlY3OC41Yy04LjQgMC0xNiAxLjgtMjIuNiA1LjYtMjguMSAxNi4yLTM0LjQgNjYuNy0xOS45IDEzMC4xLTYyLjIgMTkuMi0xMDIuNyA0OS45LTEwMi43IDgyLjMgMCAzMi41IDQwLjcgNjMuMyAxMDMuMSA4Mi40LTE0LjQgNjMuNi04IDExNC4yIDIwLjIgMTMwLjQgNi41IDMuOCAxNC4xIDUuNiAyMi41IDUuNiAyNy41IDAgNjMuNS0xOS42IDk5LjktNTMuNiAzNi40IDMzLjggNzIuNCA1My4yIDk5LjkgNTMuMiA4LjQgMCAxNi0xLjggMjIuNi01LjYgMjguMS0xNi4yIDM0LjQtNjYuNyAxOS45LTEzMC4xIDYyLTE5LjEgMTAyLjUtNDkuOSAxMDIuNS04Mi4zem0tMTMwLjItNjYuN2MtMy43IDEyLjktOC4zIDI2LjItMTMuNSAzOS41LTQuMS04LTguNC0xNi0xMy4xLTI0LTQuNi04LTkuNS0xNS44LTE0LjQtMjMuNCAxNC4yIDIuMSAyNy45IDQuNyA0MSA3Ljl6bS00NS44IDEwNi41Yy03LjggMTMuNS0xNS44IDI2LjMtMjQuMSAzOC4yLTE0LjkgMS4zLTMwIDItNDUuMiAyLTE1LjEgMC0zMC4yLS43LTQ1LTEuOS04LjMtMTEuOS0xNi40LTI0LjYtMjQuMi0zOC03LjYtMTMuMS0xNC41LTI2LjQtMjAuOC0zOS44IDYuMi0xMy40IDEzLjItMjYuOCAyMC43LTM5LjkgNy44LTEzLjUgMTUuOC0yNi4zIDI0LjEtMzguMiAxNC45LTEuMyAzMC0yIDQ1LjItMiAxNS4xIDAgMzAuMi43IDQ1IDEuOSA4LjMgMTEuOSAxNi40IDI0LjYgMjQuMiAzOCA3LjYgMTMuMSAxNC41IDI2LjQgMjAuOCAzOS44LTYuMyAxMy40LTEzLjIgMjYuOC0yMC43IDM5Ljl6bTMyLjMtMTNjNS40IDEzLjQgMTAgMjYuOCAxMy44IDM5LjgtMTMuMSAzLjItMjYuOSA1LjktNDEuMiA4IDQuOS03LjcgOS44LTE1LjYgMTQuNC0yMy43IDQuNi04IDguOS0xNi4xIDEzLTI0LjF6TTQyMS4yIDQzMGMtOS4zLTkuNi0xOC42LTIwLjMtMjcuOC0zMiA5IC40IDE4LjIuNyAyNy41LjcgOS40IDAgMTguNy0uMiAyNy44LS43LTkgMTEuNy0xOC4zIDIyLjQtMjcuNSAzMnptLTc0LjQtNTguOWMtMTQuMi0yLjEtMjcuOS00LjctNDEtNy45IDMuNy0xMi45IDguMy0yNi4yIDEzLjUtMzkuNSA0LjEgOCA4LjQgMTYgMTMuMSAyNCA0LjcgOCA5LjUgMTUuOCAxNC40IDIzLjR6TTQyMC43IDE2M2M5LjMgOS42IDE4LjYgMjAuMyAyNy44IDMyLTktLjQtMTguMi0uNy0yNy41LS43LTkuNCAwLTE4LjcuMi0yNy44LjcgOS0xMS43IDE4LjMtMjIuNCAyNy41LTMyem0tNzQgNTguOWMtNC45IDcuNy05LjggMTUuNi0xNC40IDIzLjctNC42IDgtOC45IDE2LTEzIDI0LTUuNC0xMy40LTEwLTI2LjgtMTMuOC0zOS44IDEzLjEtMy4xIDI2LjktNS44IDQxLjItNy45em0tOTAuNSAxMjUuMmMtMzUuNC0xNS4xLTU4LjMtMzQuOS01OC4zLTUwLjYgMC0xNS43IDIyLjktMzUuNiA1OC4zLTUwLjYgOC42LTMuNyAxOC03IDI3LjctMTAuMSA1LjcgMTkuNiAxMy4yIDQwIDIyLjUgNjAuOS05LjIgMjAuOC0xNi42IDQxLjEtMjIuMiA2MC42LTkuOS0zLjEtMTkuMy02LjUtMjgtMTAuMnpNMzEwIDQ5MGMtMTMuNi03LjgtMTkuNS0zNy41LTE0LjktNzUuNyAxLjEtOS40IDIuOS0xOS4zIDUuMS0yOS40IDE5LjYgNC44IDQxIDguNSA2My41IDEwLjkgMTMuNSAxOC41IDI3LjUgMzUuMyA0MS42IDUwLTMyLjYgMzAuMy02My4yIDQ2LjktODQgNDYuOS00LjUtLjEtOC4zLTEtMTEuMy0yLjd6bTIzNy4yLTc2LjJjNC43IDM4LjItMS4xIDY3LjktMTQuNiA3NS44LTMgMS44LTYuOSAyLjYtMTEuNSAyLjYtMjAuNyAwLTUxLjQtMTYuNS04NC00Ni42IDE0LTE0LjcgMjgtMzEuNCA0MS4zLTQ5LjkgMjIuNi0yLjQgNDQtNi4xIDYzLjYtMTEgMi4zIDEwLjEgNC4xIDE5LjggNS4yIDI5LjF6bTM4LjUtNjYuN2MtOC42IDMuNy0xOCA3LTI3LjcgMTAuMS01LjctMTkuNi0xMy4yLTQwLTIyLjUtNjAuOSA5LjItMjAuOCAxNi42LTQxLjEgMjIuMi02MC42IDkuOSAzLjEgMTkuMyA2LjUgMjguMSAxMC4yIDM1LjQgMTUuMSA1OC4zIDM0LjkgNTguMyA1MC42LS4xIDE1LjctMjMgMzUuNi01OC40IDUwLjZ6TTMyMC44IDc4LjR6Ii8+CiAgICA8Y2lyY2xlIGN4PSI0MjAuOSIgY3k9IjI5Ni41IiByPSI0NS43Ii8+CiAgICA8cGF0aCBkPSJNNTIwLjUgNzguMXoiLz4KICA8L2c+Cjwvc3ZnPg==#al5RUqUzTx
