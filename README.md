# Homelab

[![GitHub last commit](https://img.shields.io/github/last-commit/clearlybaffled/homelab)](https://github.com/clearlybaffled/homelab)
[![WTFPL](https://img.shields.io/badge/license-WTFPL-red?style=plastic)](http://www.wtfpl.net/)

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

## Infrastructure

Managed by Ansible

Prerequisites: 
 - python-3.9+
 - pip
 - virtualenv

Running the cluster install playbook
```
 virtualenv .venv
 source .venv/bin/activate
 pip install -U -r requirements.txt
 ansible-galaxy install -r requirements.yaml
 ansible-playbook infrastructure/playbooks/cluster.yml -D --private-key=/path/to/ansible/key
```

## Cluster
<br><br>


## Tech Stack

### Infrastructure

|Logo|Name|Description|Status|
|:----|:----|:----|:----|
|<img width="32" src="https://simpleicons.org/icons/ansible.svg">|[Ansible](https://www.ansible.com)|Automate bare metal provisioning and configuration|Working|
|<img width="32" src="https://cncf-branding.netlify.app/img/projects/argo/icon/color/argo-icon-color.svg">|[ArgoCD](https://argoproj.github.io/cd)|GitOps tool built to deploy applications to Kubernetes|In progress|
|<img width="32" src="https://github.com/jetstack/cert-manager/raw/master/logo/logo.png">|[cert-manager](https://cert-manager.io)|Cloud native certificate management|Planned|
|<img width="32" src="https://avatars.githubusercontent.com/u/314135?s=200&v=4">|[Cloudflare](https://www.cloudflare.com)|DNS and Tunnel|Investigating|
|<img width="32" src="https://avatars.githubusercontent.com/u/29074118?s=200&v=4">|[CRI-O](https://www.cri-o.io)|OCI - Container Runtime|In Use|
|<img width="32" src="https://www.debian.org/logos/openlogo-nd.svg">|[Debian](https://debian.org)|Base OS for Kubernetes Control plan|In Use|
|<img width="32" src="https://github.com/kubernetes-sigs/external-dns/raw/master/docs/img/external-dns.png">|[ExternalDNS](https://github.com/kubernetes-sigs/external-dns)|Synchronizes exposed Kubernetes Services and Ingresses with DNS providers|Planned|
|<img width="32" src="https://raw.githubusercontent.com/flannel-io/flannel/master/logos/flannel-glyph-color.svg">|[Flannel](https://www.github.com/flannel-io/flannel)|Kubernetes Network Plugin|In Use|
|<img width="32" src="https://grafana.com/static/img/menu/grafana2.svg">|[Grafana](https://grafana.com)|Operational dashboards|Planned|
|<img width="32" src="https://cncf-branding.netlify.app/img/projects/helm/icon/color/helm-icon-color.svg">|[Helm](https://helm.sh)|The package manager for Kubernetes|In Use|
|<img width="32" src="https://cncf-branding.netlify.app/img/projects/kubernetes/icon/color/kubernetes-icon-color.svg">|[Kubernetes](https://kubernetes.io)|Container Orchestration|Working|
|<img width="32" src="https://github.com/grafana/loki/blob/main/docs/sources/logo.png?raw=true">|[Loki](https://grafana.com/oss/loki)| Log aggregation system | Investigating |
|<img width="32" src="https://avatars.githubusercontent.com/u/60239468?s=200&v=4">| [MetalLB](https://metallb.org) | Bare metal load-balancer for Kubernetes | Investigating |
|<img width="32" src="https://avatars.githubusercontent.com/u/1412239?s=200&v=4">|[NGINX](https://www.nginx.com)|Kubernetes Ingress Controller|Investigating vs Traefik|
|<img width="32" src="https://cncf-branding.netlify.app/img/projects/prometheus/icon/color/prometheus-icon-color.svg">|[Prometheus](https://prometheus.io)|Systems monitoring and alerting toolkit|Planned|
|<img width="32" src="https://docs.renovatebot.com/assets/images/logo.png">|[Renovate](https://www.whitesourcesoftware.com/free-developer-tools/renovate)|Automatically update dependencies|Planned|
|<img width="32" src="https://vectorlogo.zone/logos/rookio/rookio-icon.svg">|[Rook Ceph](https://rook.io)|Cloud native block storage for Kubernetes|Investigating|
|<img width="32" src="https://vectorlogo.zone/logos/traefikio/traefikio-icon.svg">|[Traefik](https://traefik.io)|Cloud native ingress controller for Kubernetes|Investigating|
|<img width="32" src="https://docs.zerotier.com/img/ZeroTierIcon.png">|[ZeroTier](https://zerotier.com)|Virtual Networking that just works|In progress|

### Applications

| **Icon**|**Application**|**Category**|**Description**|**Deployment Status**|**Version**|
|--------|----------------|------------|---------------|---------------------|-----------|
| <img width="32" src="https://raw.githubusercontent.com/grocy/grocy/master/public/img/grocy_logo.svg">|   [Grocy][grocy-uri]                   |   `Services`   |       ERP Beyond your fridge      |        Planned  |  ![][grocy-badge] |
| <img width="32" src="https://github.com/hay-kot/mealie/blob/mealie-next/docs/docs/assets/img/favicon.png">| [Mealie][mealie-url] | `Services` | Recipe Manager | | | 
|<img width="32" src="https://github.com/MythTV/mythtv/raw/master/mythtv/html/images/icons/upnp_small_icon.png">|[MythTV][mythtv-url]| `Media` | Open Source Digital Video Recorder |Needs migrating| ![][mythtv-badge] |
|<img width="32" src="https://photonix.org/static/images/logo.svg">|[Photonix][photonix-url]| `Media` | Photo Management | | |
|<img width="32" src="https://nextcloud.com/wp-content/uploads/2022/10/nextcloud-logo-blue-transparent.svg">| [NextCloud][nextcloud-url] | `File Hosting` | File Hosting | | |
|<img width="32" src="https://hajimari.io/assets/logo.png">|[Hajimari][hajimari-url] | `Dashboard` | Startpage with K8S application discovery | | |


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

[grocy-badge]: https://img.shields.io/badge/linuxserver/grocy-v3.1.3-blue?logo=docker
[mythtv-badge]: https://img.shields.io/badge/mythtv-v0.27-blue