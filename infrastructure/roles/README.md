<h1><p align="center">
<a href="https://wwww.ansible.com"><img height="250" src="https://simpleicons.org/icons/ansible.svg" ></a><br/>

Infrastructure Automation with Ansible
</h1>

Much of it shamelessly ripped from [kubernetes-sigs/kubespray](https://github.com/kubernetes-sigs/kubespray/), and other homelabbers listed on the [README](../../README.md#-thank-you).
In the process, I definitely learned a lot and was able to incrementally migrate existing configurations and improve the overall layout to meet my needs.
I refactored a couple of the kubespray roles (especially download) to be more specific to the components I intended to use and remove those I didn't.

### Directory Structure
<!-- markdownlint-disable MD013 -->
```shell
$ tree -d --noreport -I "files|templates|tasks|defaults|vars|handlers|meta" infrastructure  ; tree --noreport playbooks

infrastructure
├── _shared
├── inventory
│   ├── group_vars
│   │   ├── all
│   │   └── kubectl
│   └── host_vars
│       ├── barb
│       ├── parche
│       └── tirante
├── pki
│   └── kubernetes-ca
└── roles
    ├── ca
    ├── cluster
    ├── common
    ├── containers
    │   ├── network
    │   ├── registry
    │   ├── runtime
    │   └── storage
    │       └── samba
    ├── download
    ├── dvb
    ├── kubernetes
    │   ├── client
    │   ├── control_plane
    │   ├── etcd
    │   ├── kubelet
    │   ├── node
    │   └── users
    ├── named
    ├── server
    └── workstation
playbooks
├── apps.yml
├── cluster.yml
├── create_user.yml
├── host.yml
├── reset.yml
└── storage.yml
```

## Playbook tasks

```shell
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

  play #4 (localhost): Set up cluster infrastructure services   TAGS: [infra]
    tasks:
      set_fact  TAGS: [infra]
      set_fact  TAGS: [infra]
      kubernetes/client : Create kube config dir for current/ansible become user        TAGS: [infra]
      kubernetes/client : Install windows clients       TAGS: [infra]
      Create cluster user for local controller user     TAGS: [infra]
      kubernetes/client : Write local kubeconfig        TAGS: [infra]
      kubernetes/client : Setup local binary clients    TAGS: [infra]
      kubernetes/client : Prefetch helm repositories    TAGS: [infra]
      kubernetes/client : Update helm repository cache  TAGS: [infra]
      kubernetes/client : Decrypt root-ca cert on disk for cacerts param to k8s module  TAGS: [infra]
      containers/network : Check for flannel subnet file        TAGS: [infra]
      containers/network : Render kustomize template    TAGS: [infra]
      containers/network : Start Resources      TAGS: [infra]
      containers/network : Wait for flannel subnet.env file presence    TAGS: [infra]
      containers/network : Remove kustomized manifest   TAGS: [infra]

  play #5 (localhost): Start up cluster TAGS: [cluster]
    tasks:
      kubernetes/cluster : Install Applications files   TAGS: [applications, cluster]
      kubernetes/cluster : Install any Kustomization files      TAGS: [cluster, kustomize]
      kubernetes/cluster : Install ArgoCD       TAGS: [argocd, cluster]
      kubernetes/cluster : Bootstrap cluster    TAGS: [bootstrap, cluster]
```
