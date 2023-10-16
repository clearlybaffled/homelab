<!-- markdownlint-disable MD040 MD024 MD046 -->
# USER    (infrastructure/roles/user)

## ENTRY POINT: kube-user

### OPTIONS (= is mandatory)

```
= groupname
        Name of the local system group
        type: str

= kube-user
        Name of the kubernetes user to create
        type: str

= username
        Name of the local system user to apply the config to
        type: str
```

## ENTRY POINT: system-user

### OPTIONS (= is mandatory)

```
= ansible_group
        ansible usergroup
        type: str

= ansible_homedir
        ansible home directory
        type: str

= ansible_user
        ansible username
        type: str

- ansible_user_ssh_key
        ssh private key for ansible user
        default: null
        type: str

- ansible_user_ssh_pubkey
        ssh public key for ansible user
        default: null
        type: str
```
