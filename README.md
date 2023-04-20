# Homelab

[![WTFPL](https://img.shields.io/badge/license-WTFPL-red?style=plastic)](http://www.wtfpl.net/)
[![GitHub last commit](https://img.shields.io/github/last-commit/clearlybaffled/homelab)](https://github.com/clearlybaffled/homelab)
[![Lint](https://github.com/clearlybaffled/homelab/actions/workflows/lint.yml/badge.svg)](https://github.com/clearlybaffled/homelab/actions/workflows/lint.yml)

Welcome to my homelab! It's a modest "cluster" with one kubernetes control plan/node with all of my self hosted services and storage, an OpnSense gateway/firewall and a couple of workstations and wireless devices.  Ultimately, this will include all applications for managing home IT systems.

## Features

- [x] Kubernetes deployment using kubeadm
- [ ] Infrastructure Automation management 
- [ ] Offline Root CA
- [ ] Manage cluster state and apps using GitOps
- [ ] Templated/automated server provisioning
- [ ] FreeIPA server
- [ ] RADIUS server
- [ ] Offsite access via VPN

## Getting Started

```shell
$ virtualenv .venv
$ source .venv/bin/activate
$ pip install -U -r requirements.txt
$ ansible-playbook infrastructure/playbooks/cluster.yml --private-key=/path/to/ansible/key
```

## Layout

- Location: America / North East
- Network:
  - ISP: Verizon FIOS (100MB/100MB)
  - WiFi: Netgear R6700 with DD-WRT
  - Switch: Cisco Catalyst 3750-X 48 port 10/100/1000 PoE
  - Gateway/Firewall: OpnSense 23
<p>Custom build boxes:</p>

|Hostname|Use(s)|Hardware|RAM|Storage|Other|
|:-------|:-----|:--------|:--|:------|:----|
|`growler`|Gateway/Firewall| ASUS Z170-M Pentium G440 3.3GHz| 8GB| 250GB NVMe ||
|`parche`|Server|ASUS Z170-A i7-6700 4.0GHz|32GB|- 250GB SSD<br/>- 24TB HDDs| Happauge 1609 WinTV-quadHD tuner|
|`barb`|Desktop|Gigabyte Z370 AORUS Intel i5-8600K @ 3.60 GHz| 64GB | - 500GB NVMe<br/>- 250GB SSD| Zotac GeForce GTX 1660 Super 6GB GDDR6|
|`seawolf`|Laptop|Dell XPS 13|16GB|250GB HDD||

  Host naming conventions. All of the physical and virtual hosts are named for the [WW2 submarines commanded][ww2-sub-moh-uri] by a [Congressional Medal of Honor](https://mohmuseum.org/the-medal/) recipient. The Kubernetes cluster is named `gato`  for the first major class of submarines built by the U.S. for use in WW2. I wanted to name something `wahoo`, after [one][wahoo-uri] of the most succesful and prolific submarines of the pacific theater, but she did not meet the requirement of having been commanded by a MoH recipient. So, anything inside the cluster that gets named will be a Gato-class submarine. Maybe the hajimari homepage, but we're not quite there yet ...

## Tech Stack

### Infrastructure

|Logo|Name|Description|Status|
|:----|:----|:----|:----|
|<img width="32" src="https://simpleicons.org/icons/ansible.svg">|[Ansible](https://www.ansible.com)|Automate bare metal provisioning and configuration|Working|
|<img width="32" src="https://cncf-branding.netlify.app/img/projects/argo/icon/color/argo-icon-color.svg">|[ArgoCD](https://argoproj.github.io/cd)|GitOps tool built to deploy applications to Kubernetes|In progress|
|<img width="32" src="https://github.com/jetstack/cert-manager/raw/master/logo/logo.png">|[cert-manager](https://cert-manager.io)|Cloud native certificate management|Planned|
|<img width="32" src="https://avatars.githubusercontent.com/u/314135?s=200&v=4">|[Cloudflare](https://www.cloudflare.com)|DNS and Tunnel|Investigating|
|<img width="32" src="https://avatars.githubusercontent.com/u/29074118?s=200&v=4">|[CRI-O](https://www.cri-o.io)|OCI - Container Runtime|In Use|
|<img width="32" src="https://www.debian.org/logos/openlogo-nd.svg">|[Debian](https://debian.org)|Base OS for Kubernetes Control plane|In Use|
|<img width="32" src="https://raw.githubusercontent.com/flannel-io/flannel/master/logos/flannel-glyph-color.svg">|[Flannel](https://www.github.com/flannel-io/flannel)|Kubernetes Network Plugin|In Use|
|<img width="32" src="https://grafana.com/static/img/menu/grafana2.svg">|[Grafana](https://grafana.com)|Operational dashboards|Planned|
|<img width="32" src="https://cncf-branding.netlify.app/img/projects/helm/icon/color/helm-icon-color.svg">|[Helm](https://helm.sh)|The package manager for Kubernetes|In Use|
|<img width="32" src="https://cncf-branding.netlify.app/img/projects/kubernetes/icon/color/kubernetes-icon-color.svg">|[Kubernetes](https://kubernetes.io)|Container Orchestration|Working|
|<img width="32" src="https://cncf-branding.netlify.app/img/projects/prometheus/icon/color/prometheus-icon-color.svg">|[Prometheus](https://prometheus.io)|Systems monitoring and alerting toolkit|Planned|
|<img width="32" src="https://vectorlogo.zone/logos/traefikio/traefikio-icon.svg">|[Traefik](https://traefik.io)|Cloud native ingress controller for Kubernetes|In progress|
|<img width="32" src="https://docs.zerotier.com/img/ZeroTierIcon.png">|[ZeroTier](https://zerotier.com)|Virtual Networking that just works|In progress|

### Applications

| **Icon**|**Application**|**Category**|**Description**|**Deployment Status**|**Version**|
|--------|----------------|------------|---------------|---------------------|-----------|
| <img width="32" src="https://raw.githubusercontent.com/grocy/grocy/master/public/img/grocy_logo.svg">|   [Grocy][grocy-uri]                   |   `Services`   |       ERP Beyond your fridge      |        Planned  |  ![][grocy-badge] |
| <img width="32" src="https://github.com/hay-kot/mealie/raw/mealie-next/docs/docs/assets/img/favicon.png">| [Mealie][mealie-url] | `Services` | Recipe Manager | | | 
|<img width="32" src="https://github.com/MythTV/mythtv/raw/master/mythtv/html/images/icons/upnp_small_icon.png">|[MythTV][mythtv-url]| `Media` | Open Source Digital Video Recorder |Needs migrating| ![][mythtv-badge] |
|<img width="32" src="https://photonix.org/static/images/logo.svg">|[Photonix][photonix-url]| `Media` | Photo Management | | |
|<img width="32" src="https://nextcloud.com/wp-content/uploads/2022/10/nextcloud-logo-blue-transparent.svg">| [NextCloud][nextcloud-url] | `File Sharing` | File Hosting | | |
|<img width="32" src="https://hajimari.io/assets/logo.png">|[Hajimari][hajimari-url] | `Dashboard` | Startpage with K8S application discovery | | |
|<img width="32" src="https://github.com/paperless-ngx/paperless-ngx/raw/dev/docs/assets/favicon.png">|[Paperless-ngx][paperless-uri] | `File Sharing` | Document Management System | | |
|<img width="32" src="https://github.com/kovidgoyal/calibre/raw/master/icons/calibre.png">|[Calibre][calibre-uri]| `Media` | e-book Manager | | |
|<img width="32" src="https://avatars.githubusercontent.com/u/2131270?s=200&v=4">|[qBittorrent][qbittorrent-uri]| `Meida` | Torrent client | | | 
|<img width="32" src="https://avatars.githubusercontent.com/u/44905828?s=200&v=4">|[NetBox][netbox-uri]| `Services`| Full-scale network inventory | | |
|<img width="32" src="https://github.com/metabrainz/design-system/raw/master/brand/logos/ListenBrainz/SVG/ListenBrainz_logo_no_text.svg">|[ListenBrainz][listenbrainz-uri]| `Media` | Open Source scrobbler | | | 

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


[grocy-uri]: https://github.com/grocy/grocy
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

[wahoo-uri]: https://en.wikipedia.org/wiki/USS_Wahoo_(SS-238)
[ww2-sub-moh-uri]: https://www.navalsubleague.org/links/historymuseums/submarine-force-medal-honor-recipients/

[grocy-badge]: https://img.shields.io/badge/linuxserver/grocy-v3.1.3-blue?logo=docker
[mythtv-badge]: https://img.shields.io/badge/mythtv-v0.27-blue
