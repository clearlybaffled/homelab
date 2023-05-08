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
|:-------|:-----|:--------|:--|:------|:----|
|`growler`|Gateway/Firewall| ASUS Z170-M Pentium G440 3.3GHz| 8GB| 250GB NVMe ||
|`parche`|Server|ASUS Z170-A i7-6700 4.0GHz|32GB|- 250GB SSD<br/>- 24TB HDDs| Happauge 1609 WinTV-quadHD tuner|
|`barb`|Desktop|Gigabyte Z370 AORUS Intel i5-8600K @ 3.60 GHz| 64GB | - 500GB NVMe<br/>- 250GB SSD| Zotac GeForce GTX 1660 Super 6GB GDDR6|
|`seawolf`|Laptop|Dell XPS 13|16GB|250GB HDD||

  Host naming conventions. All of the physical and virtual hosts are named for the [WW2 submarines commanded](ww2-sub-moh-uri) by a [Congressional Medal of Honor](https://mohmuseum.org/the-medal/) recipient. The Kubernetes cluster is named `gato`  for the first major class of submarines built by the U.S. for use in WW2. I wanted to name something `wahoo`, after [one](wahoo-uri) of the most succesful and prolific submarines of the pacific theater, but she did not meet the requirement of having been commanded by a MoH recipient. So, anything inside the cluster that gets named will be a Gato-class submarine. Maybe the hajimari homepage, but we're not quite there yet ...


## Code Layout

```
├── README.md
├── inventory
│   ├── group_vars
│   │   └── all
│   ├── host_vars
│   │   ├── all.yml
│   │   ├── barb
│   │   └── parche
│   └── inventory.ini
├── playbooks
│   ├── cluster.yml
│   └── host.yml
└── roles
    ├── common
    ├── containers
    ├── download
    ├── dvb
    ├── kubernetes
    │   ├── client
    │   ├── cluster
    │   ├── control_plane
    │   ├── etcd
    │   ├── kubelet
    │   ├── node
    │   └── users
    ├── named
    ├── server
    └── workstation
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
# Skipping for now
# $ ansible-galaxy install -r requirements.yaml
$ ansible-playbook infrastructure/playbooks/cluster.yml -D --private-key=/path/to/ansible/key
```

## Playbook tasks 

```
$ ansible-playbook --list-tasks playbooks/cluster.yml

playbook: playbooks/cluster.yml

  play #1 (k8s_cluster): Gather Cluster Facts   TAGS: []
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
      kubernetes/kubelet : Write kubelet systemd init file      TAGS: [node]
      kubernetes/kubelet : flush_handlers and reload-systemd    TAGS: [node]
      kubernetes/kubelet : Enable kubelet       TAGS: [node]

  play #3 (kube_control_plane): Install control plane   TAGS: [control_plane]
    tasks:
      kubernetes/control_plane : Install kubeadm.config file    TAGS: [control_plane]
      kubernetes/control_plane : kubeadm | Check if kubeadm has already run     TAGS: [control_plane]
      kubernetes/control_plane : Create control plane with kubeadm      TAGS: [control_plane]
      kubernetes/control_plane : Apply crun Runtime class       TAGS: [control_plane]
      Create cluster user for ansible   TAGS: [control_plane]
      kubernetes/control_plane : Write kubeconfig       TAGS: [control_plane]

  play #4 (kube_control_plane[0]): Configure local binaries for cluster admin   TAGS: [client]
    tasks:
      kubernetes/client : Set some facts        TAGS: [client]
      kubernetes/client : Create kube config dir for current/ansible become user        TAGS: [client]
      kubernetes/client : Install windows clients       TAGS: [client]
      Create cluster user for local controller user     TAGS: [client]
      kubernetes/client : Write local kubeconfig        TAGS: [client]
      kubernetes/client : Setup local binary clients    TAGS: [client]

  play #5 (localhost): Register CNI pluin       TAGS: [cni]
    tasks:
      containers/network : Render kustomize template    TAGS: [cni]
      containers/network : Start Resources      TAGS: [cni]
      containers/network : Wait for flannel subnet.env file presence    TAGS: [cni]

  play #6 (localhost): Start up cluster TAGS: [cluster]
    tasks:
      kubernetes/cluster : Make sure ArgoCD manifest version matches in cluster kustomize       TAGS: [cluster]
      kubernetes/cluster : Create argocd namespace      TAGS: [cluster]
      kubernetes/cluster : Apply argocd manifest        TAGS: [cluster]
      kubernetes/cluster : Wait for all argocd crds to load     TAGS: [cluster]
      kubernetes/cluster : Kick off cluster boostrap    TAGS: [cluster]
```
