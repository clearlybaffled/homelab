# Infrastructure
## Ansible

Prerequisites: 
 - python-3.9+
 - pip
 - virtualenv

```
$ cd infrastructure/ansible
$ virtualenv --python=$(which python3) .venv
$ pip install -U -r requirements.txt
$ ansible-playbook playbooks/cluster.yml -D -K
```

# Cluster