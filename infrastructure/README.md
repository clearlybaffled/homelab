<p align="center">
<a href="https://wwww.ansible.com"><img height="250" src="https://simpleicons.org/icons/ansible.svg"></a><br/>

# Infrastructure Automation with Ansible

Much of it shamelesesly ripped from [kubernetes-sigs/kubespray](https://github.com/kubernetes-sigs/kubespray/), and other homelabbers listed below. In the process, I definitely learned a lot and was able to incrementally migrate existing configurations and improve the overall layout to meet my needs.  I refactored a couple of the kubespray roles (especially download) to be more specific to the components I intended to use and remove those I didn't.

## Layout 

### Hardware

- Location: America / North East
- Network:
  - ISP: Verizon FIOS (100MB/100MB)
  - WiFi: Netgear R6700 with DD-WRT
  - Switch: Cisco Catalyst 3750-X 48 port 10/100/1000 PoE
  - Gateway/Firewall: OpnSense 23
<p>Custom built boxes:</p>

|Hostname|Use(s)|Hardware|RAM|Storage|Other|
|:-------|:-----|:-------|:--|:------|:----|
|`growler`|Gateway/Firewall| ASUS Z170-M Pentium G440 3.3GHz| 8GB| 250GB NVMe ||
|`parche`|Server|ASUS Z170-A i7-6700 4.0GHz|32GB|- 250GB SSD<br/>- 24TB HDDs| Happauge 1609 WinTV-quadHD tuner|
|`barb`|Desktop|Gigabyte Z370 AORUS Intel i5-8600K @ 3.60 GHz| 64GB | - 500GB NVMe<br/>- 250GB SSD| Zotac GeForce GTX 1660 Super 6GB GDDR6|
|`seawolf`|Laptop|Dell XPS 13|16GB|250GB HDD||

  Host naming conventions. All of the physical and virtual hosts are named for the [WW2 submarines commanded](ww2-sub-moh-uri) by a [Congressional Medal of Honor](https://mohmuseum.org/the-medal/) recipient. The Kubernetes cluster is named `gato`  for the first major class of submarines built by the U.S. for use in WW2. I wanted to name something `wahoo`, after [one](wahoo-uri) of the most succesful and prolific submarines of the pacific theater, but she did not meet the requirement of having been commanded by a MoH recipient. So, anything inside the cluster that gets named will be a Gato-class submarine. Maybe the hajimari homepage, but we're not quite there yet ...


## Code Layout

```
$ tree -d -I "files|templates|tasks|defaults|vars|handlers|meta" infrastructure

├── inventory
│   ├── group_vars
│   │   ├── all
│   │   └── kubectl
│   └── host_vars
│       ├── barb
│       └── parche
├── pki
│   ├── kubernetes-ca
│   └── root-ca
├── roles
│   ├── ca
│   ├── cluster
│   │   ├── cert-manager
│   │   ├── coredns
│   │   ├── dashboard
│   │   ├── local_path_provisioner
│   │   ├── metallb
│   │   ├── setup
│   │   ├── traefik
│   │   └── vault
│   ├── common
│   ├── containers
│   │   ├── network
│   │   ├── registry
│   │   └── runtime
│   ├── download
│   ├── dvb
│   ├── kubernetes
│   │   ├── cluster
│   │   ├── control_plane
│   │   ├── etcd
│   │   ├── kubelet
│   │   ├── node
│   │   └── users
│   ├── named
│   ├── server
│   └── workstation
└── _shared
```

## Usage guide

Prerequisites: 
 - python-3.9+
 - pip
 - virtualenv

Configure cluster using the playbook
```shell
$ virtualenv .venv
$ source .venv/bin/activate
$ pip install -U -r requirements.txt
# Don't think this is needed
# $ ansible-galaxy install -r requirements.yaml
$ ansible-playbook playbooks/cluster.yml
```

## Playbook tasks 

```
$ ansible-playbook --list-tasks playbooks/cluster.yml

playbook: playbooks/cluster.yml

  play #1 (k8s_cluster,localhost): Gather Cluster Facts TAGS: [always]
    tasks:

  play #2 (kube_node): Kubernetes Node setup    TAGS: [node]
    tasks:
      kubernetes/node : Install k8s system packages     TAGS: [node]
      kubernetes/node : Create kube_cert_group  TAGS: [node]
      kubernetes/node : Create kube group       TAGS: [node]
      kubernetes/node : Create user     TAGS: [node]
      kubernetes/node : Add ansible_user to kube_group  TAGS: [node]
      kubernetes/node : Ensure ansible_user has a ~/.kube directory     TAGS: [node]
      kubernetes/node : Enable kernel modules now       TAGS: [node]
      kubernetes/node : Enable kernel modules on boot   TAGS: [node]
      kubernetes/node : Set sysctls     TAGS: [node]
      kubernetes/node : Permissive SELinux      TAGS: [node]
      kubernetes/node : Load os specific tasks  TAGS: [node]
      kubernetes/node : Ensure kube_config_dir exists   TAGS: [node]
      kubernetes/node : Create cni directories  TAGS: [node]
      download : download | Prepare working directories and variables   TAGS: [download, node, upload]
      download : download | Get kubeadm binary and list of required images      TAGS: [download, node, upload]
      download : download | Download files / images     TAGS: [download, node]
      containers/runtime : containers/runtime | Create containers posix group   TAGS: [node]
      containers/runtime : cri-o | make sure needed folders exist in the system TAGS: [node]
      containers/runtime : cri-o | install cri-o config TAGS: [node]
      containers/runtime : cri-o | install config.json  TAGS: [node]
      containers/runtime : cri-o | copy service file    TAGS: [node]
      containers/runtime : cri-o | copy default policy  TAGS: [node]
      containers/runtime : cri-o | copy mounts.conf     TAGS: [node]
      containers/runtime : cri-o | create directory for oci hooks       TAGS: [node]
      containers/runtime : cri-o | set overlay driver   TAGS: [node]
      containers/runtime : cri-o | set metacopy mount options correctly TAGS: [node]
      containers/runtime : cri-o | create directory registries configs  TAGS: [node]
      containers/runtime : cri-o | write registries configs     TAGS: [node]
      containers/runtime : cri-o | configure unqualified registry settings      TAGS: [node]
      containers/runtime : cri-o | write cri-o proxy drop-in    TAGS: [node]
      containers/runtime : cri-o | find man files       TAGS: [node]
      containers/runtime : cri-o | make man dirs        TAGS: [node]
      containers/runtime : cri-o | copy man files       TAGS: [node]
      containers/runtime : cri-o | configure the uid/gid space for user namespaces      TAGS: [node]
      containers/runtime : cri-o | ensure crio service is started and enabled   TAGS: [node]
      containers/runtime : cri-o | trigger service restart only when needed     TAGS: [node]
      containers/runtime : cri-o | verify that crio is running  TAGS: [node]
      containers/runtime : cri-o | Set socket group owner       TAGS: [node]
      containers/runtime : crictl | Install config      TAGS: [node]
      containers/runtime : Get crictl completion        TAGS: [node]
      containers/runtime : Install crictl completion    TAGS: [node]
      download : download | Prepare working directories and variables   TAGS: [download, node, upload]
      download : download | Get kubeadm binary and list of required images      TAGS: [download, node, upload]
      download : download | Download files / images     TAGS: [download, node]
      kubernetes/kubelet : look up crio cgroup driver   TAGS: [node]
      kubernetes/kubelet : set kubelet_cgroup_driver_detected fact for crio     TAGS: [node]
      kubernetes/kubelet : Set kubelet api version to v1beta1   TAGS: [node]
      kubernetes/kubelet : create kubelet.service.d     TAGS: [node]
      kubernetes/kubelet : Write kubelet environment config file (kubeadm)      TAGS: [node]
      kubernetes/kubelet : Write kubelet config file    TAGS: [node]
      kubernetes/kubelet : Write kubelet systemd init file      TAGS: [node]
      kubernetes/kubelet : flush_handlers and reload-systemd    TAGS: [node]
      kubernetes/kubelet : Enable kubelet       TAGS: [node]

  play #3 (kube_control_plane): Install control plane   TAGS: [control_plane]
    tasks:
      kubernetes/control_plane : kubeadm | Check if kubeadm has already run     TAGS: [control_plane]
      kubernetes/control_plane : kubeadm | aggregate all SANs   TAGS: [control_plane, facts]
      kubernetes/control_plane : Install kubeadm.config file    TAGS: [control_plane]
      kubernetes/control_plane : kubeadm | Install Kubernetes CA certs  TAGS: [control_plane]
      kubernetes/control_plane : kubeadm | Init certs phase     TAGS: [control_plane]
      kubernetes/control_plane : kubeadm | Append ca cert to apiserver cert     TAGS: [control_plane]
      kubernetes/control_plane : kubeadm | Finish kubeadm init  TAGS: [control_plane]

  play #4 (localhost): Setup cluster infrastructure services    TAGS: [infra]
    tasks:
      set_fact  TAGS: [infra]
      set_fact  TAGS: [infra]
      cluster/setup : Create kube config dir for current/ansible become user    TAGS: [infra]
      cluster/setup : Install windows clients   TAGS: [infra]
      Create cluster user for local controller user     TAGS: [infra]
      cluster/setup : Write local kubeconfig    TAGS: [infra]
      cluster/setup : Setup local binary clients        TAGS: [infra]
      cluster/setup : Prefetch helm repositories        TAGS: [infra]
      cluster/setup : Update helm repository cache      TAGS: [infra]
      containers/network : Check for flannel subnet file        TAGS: [infra]
      containers/network : Render kustomize template    TAGS: [infra]
      containers/network : Start Resources      TAGS: [infra]
      containers/network : Wait for flannel subnet.env file presence    TAGS: [infra]
      containers/network : Remove kustomized manifest   TAGS: [infra]
      cluster/coredns : Install manifests       TAGS: [coredns, infra]
      cluster/metallb : Kubernetes Apps | Create MetalLB resources      TAGS: [infra]
      cluster/metallb : Kubernetes Apps | Wait for MetalLB controller to be running     TAGS: [infra]
      cluster/metallb : Kubernetes Apps | Install and configure MetalLB TAGS: [infra]
      cluster/traefik : Install traefik helm repo       TAGS: [infra]
      cluster/traefik : Install traefik helm chart      TAGS: [infra]
      cluster/dashboard : Kubernetes Apps | Start dashboard     TAGS: [infra]
      cluster/local_path_provisioner : Local Path Provisioner | Create addon dir        TAGS: [infra]
      cluster/local_path_provisioner : Local Path Provisioner | Create claim root dir   TAGS: [infra]
      cluster/local_path_provisioner : Local Path Provisioner | Render Template TAGS: [infra]
      cluster/local_path_provisioner : Local Path Provisioner | Insert extra templates to Local Path Provisioner templates list for PodSecurityPolicy   TAGS: [infra]
      cluster/local_path_provisioner : Local Path Provisioner | Create manifests        TAGS: [infra]
      cluster/local_path_provisioner : Local Path Provisioner | Apply manifests TAGS: [infra]
      cluster/cert-manager : Install Cert Manager       TAGS: [infra]
      cluster/cert-manager : Install Trust Manager      TAGS: [infra]
      cluster/cert-manager : Configure ClusterIssuer    TAGS: [infra]

  play #5 (localhost): Start up cluster TAGS: [cluster]
    tasks:
      kubernetes/cluster : Install Kustomization files for each app     TAGS: [cluster, manifests]
      kubernetes/cluster : Commit changes to Kustomization files, if necessary  TAGS: [cluster]
      kubernetes/cluster : Create argocd namespace      TAGS: [cluster]
      kubernetes/cluster : Start ArgoCD TAGS: [cluster]
      kubernetes/cluster : Configure ArgoCD to use helm with kustomize  TAGS: [cluster]
      kubernetes/cluster : argocd server insecure       TAGS: [cluster]
```

[wahoo-uri]: https://en.wikipedia.org/wiki/USS_Wahoo_(SS-238)
[ww2-sub-moh-uri]: https://www.navalsubleague.org/links/historymuseums/submarine-force-medal-honor-recipients/