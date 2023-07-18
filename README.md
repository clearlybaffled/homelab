# Homelab

[![WTFPL](https://img.shields.io/github/license/clearlybaffled/homelab?style=plastic)](http://www.wtfpl.net/)
[![GitHub last commit](https://img.shields.io/github/last-commit/clearlybaffled/homelab/main?style=plastic)](https://github.com/clearlybaffled/homelab/commits/main)
[![Lint](https://github.com/clearlybaffled/homelab/actions/workflows/lint.yml/badge.svg)](https://github.com/clearlybaffled/homelab/actions/workflows/lint.yml)
![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/clearlybaffled/homelab?style=plastic)

Welcome to my homelab! It's a modest "cluster" with one kubernetes control plan/node with all of my self hosted services and storage, an OpnSense gateway/firewall and a couple of workstations and wireless devices.  Ultimately, this will include all applications for managing home IT systems.

## Features

- [x] Kubernetes deployment using kubeadm
- [x] Infrastructure Automation management 
- [x] Offline Root CA
- [x] Manage cluster state and apps using GitOps
- [x] Automated server provisioning
- [ ] FreeIPA server
- [ ] RADIUS server
- [ ] Offsite access via VPN

## Getting Started

```shell
$ virtualenv .venv
$ source .venv/bin/activate
$ pip install -U -r requirements.txt
$ ansible-playbook infrastructure/cluster.yml
```
## Tech Stack

### Infrastructure

|Logo|Name|Description|
|:----|:----|:----|
|<img width="32" src="https://simpleicons.org/icons/ansible.svg">|[Ansible](https://www.ansible.com)|Automate bare metal provisioning and configuration|
|<img width="32" src="https://cncf-branding.netlify.app/img/projects/argo/icon/color/argo-icon-color.svg">|[ArgoCD](https://argoproj.github.io/cd)|GitOps tool built to deploy applications to Kubernetes|
|<img width="32" src="https://github.com/jetstack/cert-manager/raw/master/logo/logo.png">|[cert-manager](https://cert-manager.io)|Cloud native certificate management|
|<img width="32" src="https://avatars.githubusercontent.com/u/29074118?s=200&v=4">|[CRI-O](https://www.cri-o.io)|OCI - Container Runtime|
|<img width="32" src="https://www.debian.org/logos/openlogo-nd.svg">|[Debian](https://debian.org)|Base OS for Kubernetes Control plane|
|<img width="32" src="https://raw.githubusercontent.com/flannel-io/flannel/master/logos/flannel-glyph-color.svg">|[Flannel](https://www.github.com/flannel-io/flannel)|Kubernetes Network Plugin|
|<img width="32" src="https://cncf-branding.netlify.app/img/projects/helm/icon/color/helm-icon-color.svg">|[Helm](https://helm.sh)|The package manager for Kubernetes|
|<img width="32" src="https://docs.nginx.com/nginx-ingress-controller/images/icons/NGINX-Ingress-Controller-product-icon.svg">|[Ingress-nginx](https://kubernetes.github.io/ingress-nginx/)| Ingress controller for Kubernetes using NGINX as a reverse proxy and load balancer|
|<img width="32" src="https://cncf-branding.netlify.app/img/projects/kubernetes/icon/color/kubernetes-icon-color.svg">|[Kubernetes](https://kubernetes.io)|Container Orchestration|
|<img width="32" src="https://avatars.githubusercontent.com/u/60239468?s=200&v=4">|[MetalLB](https://metallb.org)|Bare metal load-balancer for Kubernetes|
|<img width="32" src="https://cncf-branding.netlify.app/img/projects/prometheus/icon/color/prometheus-icon-color.svg">|[Prometheus](https://prometheus.io)|Systems monitoring and alerting toolkit|
|<img width="32" src="https://docs.zerotier.com/img/ZeroTierIcon.png">|[ZeroTier](https://zerotier.com)|Virtual Networking that just works|

### Applications

| **Icon**|**Application**|**Category**|**Description**|**Deployment Status**|**Version**|
|--------|----------------|------------|---------------|---------------------|-----------|
|<img width="32" src="https://www.mysql.com/common/logos/logo-mysql-170x115.png">|[MySQL][mysql-uri]| `Database` | SQL Database | Deployed | [![][mysql-badge]][mysql-img]
|<img width="32" src="https://wiki.postgresql.org/images/a/a4/PostgreSQL_logo.3colors.svg">| [PostgreSQL][postgres-uri] | `Database` | via [Cloudnative-PG][cnpg-io] operator | Deployed | [![][cnpg-badge]][cnpg-chart]
|<img width="32" src="https://redis.io/images/favicons/favicon-32x32.png">| [Redis][redis-uri] | `Database` | In-memory Key-Value store | Deployed | [![][redis-badge]][redis-img]
|<img width="32" src="https://raw.githubusercontent.com/grocy/grocy/master/public/img/logo.svg">| [Grocy][grocy-uri] | `Services` | ERP Beyond your fridge | Deployed | [![][grocy-badge]][grocy-img] |
|<img width="32" src="https://github.com/hay-kot/mealie/raw/mealie-next/docs/docs/assets/img/favicon.png">| [Mealie][mealie-url] | `Services` | Recipe Manager | | | 
|<img width="32" src="https://github.com/MythTV/mythtv/raw/master/mythtv/html/images/icons/upnp_small_icon.png">|[MythTV][mythtv-url]| `Media` | Open Source Digital Video Recorder | Moved off-cluster | ![][mythtv-badge] |
|<img width="32" src="https://photonix.org/static/images/logo.svg">|[Photonix][photonix-url]| `Media` | Photo Management | | |
|<img width="32" src="https://nextcloud.com/wp-content/uploads/2022/10/nextcloud-logo-blue-transparent.svg">| [NextCloud][nextcloud-url] | `File Sharing` | File Hosting | | |
|<img width="32" src="https://hajimari.io/assets/logo.png">|[Hajimari][hajimari-url] | `Dashboard` | Startpage with K8S application discovery | Deployed | ![][hajimari-badge] |
|<img width="32" src="https://grafana.com/static/img/menu/grafana2.svg">|[Grafana](https://grafana.com)| `Dashboard` | Operational dashboards | Deployed | ![][grafana-badge] |
|<img width="32" src="https://github.com/paperless-ngx/paperless-ngx/raw/dev/docs/assets/favicon.png">|[Paperless-ngx][paperless-uri] | `File Sharing` | Document Management System | Deployed| |
|<img width="32" src="https://github.com/kovidgoyal/calibre/raw/master/icons/calibre.png">|[Calibre][calibre-uri]| `Media` | e-book Manager | | |
|<img width="32" src="https://avatars.githubusercontent.com/u/2131270?s=200&v=4">|[qBittorrent][qbittorrent-uri]| `Meida` | Torrent client | | | 
|<img width="32" src="https://avatars.githubusercontent.com/u/44905828?s=200&v=4">|[NetBox][netbox-uri]| `Services`| Full-scale network inventory | | |
|<img width="32" src="https://github.com/metabrainz/design-system/raw/master/brand/logos/ListenBrainz/SVG/ListenBrainz_logo_no_text.svg">|[ListenBrainz][listenbrainz-uri]| `Media` | Open Source scrobbler | | | 
|<img width="32" src="https://simpleicons.org/icons/vault.svg">|[Vault](https://www.vaultproject.io)| `Services` | Secrets and encryption management system| | |

## Thank you!
- https://github.com/bjw-s/home-ops
- https://github.com/onedr0p/home-ops
- https://github.com/khuedoan/homelab
- https://github.com/gruberdev/homelab
- https://github.com/RickCoxDev/home-cluster
- https://github.com/billimek/k8s-gitops
- https://github.com/blackjid/k8s-gitops
- https://github.com/carpenike/k8s-gitops
- [K8s-At-Home Project](https://k8s-at-home.com)  

<details>
<summary>Repository Stats</summary>
<br/>

![Alt](https://repobeats.axiom.co/api/embed/d99fddfc840ac253fd4c4975137e1561dfaf128d.svg "Repobeats analytics image")

</details>

[grocy-uri]: https://github.com/grocy/grocy
[grocy-img]: https://hub.docker.com/r/linuxserver/grocy
[photonix-url]: https://photonix.org/
[mythtv-url]: https://www.mythtv.org
[nextcloud-url]: https://www.nextcloud.com
[hajimari-url]:https://hajimari.io/
[mealie-url]:https://mealie.io/
[paperless-uri]: https://docs.paperless-ngx.com/
[calibre-uri]: https://calibre-ebook.com/
[qbittorrent-uri]: https://www.qbittorrent.org/
[netbox-uri]: https://netbox.dev
[listenbrainz-uri]: https://listenbrainz.org
[mysql-uri]: https://www.mysql.com
[mysql-img]: https://hub.docker.com/r/bitnami/mysql
[postgres-uri]: https://www.postgresql.org
[cnpg-io]:https://cloudnative-pg.io/
[redis-uri]: https://redis.io
[redis-img]: https://hub.docker.com/r/bitnami/redis

[grocy-badge]: https://img.shields.io/badge/linuxserver/grocy-v3.3.2-blue?logo=docker
[mythtv-badge]: https://img.shields.io/badge/mythtv-v0.33-blue
[hajimari-badge]: https://img.shields.io/badge/hajimari-v2.0.2-blue
[grafana-badge]: https://img.shields.io/badge/grafana-v9.5.2-blue?logo=grafana
[mysql-badge]: https://img.shields.io/badge/bitnami/mysql-v8.0.33-blue?logo=docker
[cnpg-badge]: https://img.shields.io/badge/cloudnative--pg%2Fcloudnative--pg-v1.20.0-blue?logo=artifacthub
[cnpg-chart]: https://artifacthub.io/packages/helm/cloudnative-pg/cloudnative-pg
[redis-badge]: https://img.shields.io/badge/bitnami/redis-v7.0.11-blue?logo=docker
