<h1><p align="center">
<a href="https://wwww.ansible.com"><img height="200" src="https://simpleicons.org/icons/ansible.svg" ></a>
&nbsp;
<a href="https://www.terraform.io"><img height="200" src="https://api.iconify.design/logos/terraform-icon.svg"></a>
</p>
Infrastructure + Automation with Ansible and Terraform
</h1>

Much of it shamelessly ripped from [kubernetes-sigs/kubespray](https://github.com/kubernetes-sigs/kubespray/), and other homelabbers listed on the [README](../README.md#-thank-you).

In the process, I definitely learned a lot and was able to incrementally migrate existing configurations and improve the overall layout to meet my needs.
I refactored a couple of the kubespray roles (especially download) to be more specific to the components I intended to use and remove those I didn't.

## Infrastructure Layout

### Network Diagram

![](/docs/Homelab.png)

### Hardware

- Location: America / North East
- Network:
  - ISP: Verizon FIOS (100MB/100MB)
  - WiFi: Netgear R6700 with DD-WRT
  - Switch: Cisco Catalyst 3750-X 48 port 10/100/1000 PoE
  - Gateway/Firewall: OpnSense 23.7

<!-- markdownlint-disable-next-line MD013 -->
### <img src="https://www.sublant.usff.navy.mil/Portals/47/Images/Gold%20Dolphins.gif?ver=2020-09-11-162749-663" height=12> Host naming conventions

Between college and getting a real job, I served as a submarine officer in the US Navy, something I took great pride in.
As a homage to that, I named all physical and virtual hosts for [WW2 submarines commanded][ww2-sub-moh-uri] by a [Congressional Medal of Honor](https://mohmuseum.org/the-medal/) recipient.

I also have names of two boats that did not meet the requirements of being commanded by a MoH recipient that I wanted to use anyway, so I reserved them for more "logical" assignments as opposed to the physical assignments of hosts/VMs:

- The kubernetes cluster is named `seawolf`, a boat with a very successful WW2 record and a name with quite the [prolific record][seawolf-wiki] throughout the history of the submarine force.
- I also want to name something `wahoo`, after [another][wahoo-uri] of the most highly successful and aggressive submarines of the Pacific theater, but I felt Seawolf's record lead it to deserve the cluster name. I'll come up with something...

### Systems

|Hostname|Use(s)|Operating System|Hardware|RAM|Storage|Other|
|:---------|:-----|:---------------|:-------|:---|:------------|:---------|
|`growler` [<sup>1</sup>][growler-moh]|Gateway/Firewall| FreeBSD 13.2-RELEASE-p3 | ASUS Z170-M<br/>Pentium G440 @ 3.3GHz| 8GB| 250GB NVMe ||
|`parche` [<sup>2</sup>][parche-moh]|Server|Debian 12 |ASUS Z170-A<br/>i7-6700 @ 4.0GHz|32GB|<ul><li>250GB SSD<li>24TB (4x) HDDs</ul>| Happauge 1609 WinTV-quadHD tuner|
|`barb` [<sup>3</sup>][barb-moh]|Workstation|Windows 10 Pro|Gigabyte Z370 AORUS<br/>Intel i5-8600K @ 3.60 GHz| 64GB | 500GB NVMe | Zotac GeForce GTX 1660 Super 6GB GDDR6|
|`tirante` [<sup>4</sup>][tirante-moh]|Workstation|Ubuntu 22.04 LTS| WSL version 2 on `barb`| 32GB | 375MB | |
|`sculpin` [<sup>5</sup>][sculpin-moh]|Workstation|Windows 10 Home|Dell XPS 13|16GB|250GB HDD||
|`tang` [<sup>6</sup>][tang-moh]|Server|Fedora 38 (Cloud)|Qemu Virtual Host|4GB|5GB qcow2||
| `harder` [<sup>7</sup>][harder-moh]|Server||Raspberry Pi 3B A1.2GhZ|1GB|16GB SDCard||

### Network/Other Devices

The rest are simply named by function and location: {function}-{floor}-{room}.
It harkens back to a time when I had delusions of grandeur of having network devices all over the house.

|Hostname|Use(s)|Operating System|Hardware|
|:---------|:-----|:---------------|:-------|
|br-1-off| Border Router | | |
|cor-1-off| Core Switch | Cisco IOS 12.2.1 | Cisco Catalyst 3750X |
|ap-1-off| Access Point | DD-WRT v3.0-r35030M | Netgear R6700|
|ups| UPS| | APC |
|pdu-1-off| Power Distribution Unit| | APC|

## Usage guide

Prerequisites:

- python-3.9+
- pip
- virtualenv

Create python virtual environment in repository root

```shell
python -m venv .venv
source .venv/bin/activate
pip install -U -r requirements.txt
ansible-galaxy install -r requirements.yaml
```

Either run meta-playbook to install the entire lab ...

```shell
ansible-playbook homelab.yml
```

... or run each playbook individually

```shell
ansible-playbook playbooks/hosts.yml
ansible-playbook playbooks/cluster.yml
ansible-playbook playbooks/apps.yml
ansible-playbook playbooks/freeipa.yml
```

Main features include:

- Completely sets up a control plane host from nothing to fully running
- Switching to using localhost for tasks execution once direct access to the control plane itself is no longer needed
- Pushes templated configurations for cluster apps to [`cluster/`](../cluster/) directory and launches ArgoCD to bootstrap the cluster
- Provisions virtual hosts using Terraform and starts the IPA Server
- Package management for some windows and linux machines

Still needs to:

- Be able to handle setting up additional control plane hosts (it might, but probably doesn't). (It definitely won't join a new control plane, I'm more wondering how much of the setup was tweaked for the first host..)
- Include setup/CM for the OpnSense router/fw, and Cisco switch

## Directory Structure
<!-- markdownlint-disable MD013 -->
```shell
$ tree -P infrastructure -P playbooks* -P homelab.yml \
  -I "files|templates|tasks|defaults|vars|handlers|meta|filter*|references|scripts|cluster" \
  --matchdirs
.
├── homelab.yml
├── infrastructure
│   ├── README.md
│   ├── _shared
│   ├── inventory
│   │   ├── group_vars
│   │   │   ├── all
│   │   │   ├── ipaserver
│   │   │   ├── kubectl
│   │   │   └── workstation
│   │   └── host_vars
│   │       ├── barb
│   │       ├── localhost
│   │       ├── parche
│   │       └── tirante
│   ├── pki
│   │   └── kubernetes-ca
│   ├── roles
│   │   ├── apps
│   │   ├── ca
│   │   ├── common
│   │   ├── containers
│   │   │   ├── network
│   │   │   ├── registry
│   │   │   ├── runtime
│   │   │   └── storage
│   │   │       ├── local_path_provisioner
│   │   │       └── samba
│   │   ├── download
│   │   ├── dvb
│   │   ├── kubernetes
│   │   │   ├── client
│   │   │   ├── control_plane
│   │   │   ├── etcd
│   │   │   ├── kubelet
│   │   │   ├── node
│   │   │   └── users
│   │   ├── named
│   │   ├── server
│   │   │   └── kvm
│   │   └── workstation
│   └── terraform
│       ├── ipa
│       └── kvm
└── playbooks
    ├── apps.yml
    ├── cluster.yml
    ├── create_user.yml
    ├── freeipa.yml
    ├── host.yml
    ├── reset.yml
    └── storage.yml
```
<!-- markdownlint-enable MD013 -->

# Ansible

## Roles

- apps: manages individual configuration for applications deployed to the kubernetes cluster through ArgoCD.
  Generates various Kubernetes manifest files from templates based on the configuration and runs any custom setup tasks each app might need.
  See [cluster](../cluster/) for more information on where it all lands.
- ca: Manual certificate issuance and CA management.
  Creates "lightweight" certificate authorities using `openssl ca` and uses those to sign certificate requests and issue valid certs.
  Currently, only CA being managed is the (offline) Root CA.
  Intermediate CAs are for Kubernetes and IPA, which each manage their own certificates from there,
  so there is no need to setup any additional intermediate CAs using these tasks at this time.
- common: Some common settings, tasks, and handlers
- containers: All things container management
  - network: Start/teardown container network interface (CNI), currently flannel
  - registry: Manage a container registry. (Not in use)
  - runtime: Install, manage, teardown container runtime, currently CRI-O
  - storage: manage storage configuration. Creates some PersistentVolumes and other objects for static/local storage management
    and deploys rancher's local path provisioner. rook-ceph itself is managed as a cluster app.
- download: Manages downloads of core containers and binaries. Ripped from kubespray and heavily modified.
- dvb: Build/Install of Digital Video Broadcasting system, currently MythTV
- kubernetes: Kubernetes cluster management
  - client: Ensure a working kubectl client exists on ansible controller
  - control_plane: Bootstraps control plane using `kubeadm`
  - etcd: (not in use)
  - kubelet: Install and start kubelet as a system service
  - node: System level dependencies and settings necessary to prepare a server to run as a kubernetes node
  - users: Create kubernetes cluster role to be used by a person
- named: (deprecated) named configuration migrated from `named-chroot` from previous incarnation of `parche`
- server: Server installation and setup tasks, package management, customization settings
  - kvm: Install and manage host-level and virtual libvirt/KVM services
- workstation: package management and customizations for workstations

# Terraform

## Modules

- kvm: Basic kvm setup and base image management.
  This was intended to be a base module that other modules could inherit the libvirt connection info from,
  but terraform doesn't seem to work that way.
  I definitely didn't dig into it enough - it works for now.
- ipa: Provision and initial setup of the IPA master server before handing off to ansible to install the application

[wahoo-uri]: https://en.wikipedia.org/wiki/USS_Wahoo_(SS-238)
[ww2-sub-moh-uri]: https://www.navalsubleague.org/links/historymuseums/submarine-force-medal-honor-recipients/
[sculpin-moh]: https://www.navalsubleague.org/links/historymuseums/submarine-force-medal-honor-recipients/capt-john-p-cromwell-1943/
[harder-moh]: https://www.navalsubleague.org/links/historymuseums/submarine-force-medal-honor-recipients/cdr-samuel-d-dealey-1944/
[barb-moh]: https://www.navalsubleague.org/links/historymuseums/submarine-force-medal-honor-recipients/3864-2/
[growler-moh]: https://www.navalsubleague.org/links/historymuseums/submarine-force-medal-honor-recipients/cdr-howard-w-gilmore-1943/
[tang-moh]: https://www.navalsubleague.org/links/historymuseums/submarine-force-medal-honor-recipients/cdr-howard-w-gilmore-1943/
[parche-moh]: https://www.navalsubleague.org/links/historymuseums/submarine-force-medal-honor-recipients/cdr-lawson-p-ramage-1944/
[tirante-moh]: https://www.navalsubleague.org/links/historymuseums/submarine-force-medal-honor-recipients/cdr-george-l-street-iii-1945/
[seawolf-wiki]: https://en.wikipedia.org/wiki/USS_Seawolf
