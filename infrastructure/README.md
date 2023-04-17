<p align="center">
<a href="https://wwww.ansible.com"><img height="250" src="https://simpleicons.org/icons/ansible.svg"></a><br/>

# Infrastructure Automation with Ansible

Much of it shamelesesly ripped from [kubernetes-sigs/kubespray](https://github.com/kubernetes-sigs/kubespray/), and other homelabbers listed below. In the process, I definitely learned a lot and was able to incrementally migrate existing configurations and improve the overall layout to meet my needs.  I refactored a couple of the kubespray roles (especially download) to be more specific to the components I intended to use and remove those I didn't.

## Layout

```
├── README.md
├── _shared
│   └── networks.yaml
├── inventory
│   ├── group_vars
│   │   ├── all
│   │   └── k8s_cluster
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
    ├── container_engine
    ├── download
    ├── dvb
    ├── kubernetes
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
