# Infrastructure

## Ansible

Prerequisites: 
 - python-3.9+
 - pip
 - virtualenv

### Running the cluster install playbook
```
 virtualenv --python=$(which python3) .venv
 source .venv/bin/activate
 pip install -U -r requirements.txt
 ansible-galaxy install -r requirements.yaml
 ansible-playbook playbooks/cluster.yml -D --private-key=/path/to/ansible/key
```

# Cluster

## Argo-CD
