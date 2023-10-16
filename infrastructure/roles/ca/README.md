# CA    (infrastructure/roles/ca)

## ENTRY POINT: main - Main role entrypoint

        This is the main entrypoint for the `ca' role. Based on
        `purpose' input variable, determines which taskfile to load In
        my homelab setup, all CA management directories are stored on
        an offline crypto device, so the CA role will automatically
        manage opening and closing that device when performing
        operations

### OPTIONS (= is mandatory):
```
- purpose
        Used by main to determine which task file to run
        If not provided, runs the root-ca task
        Passes along `purpose' along with other input values to
        subsequent tasks. See other entrypoints below for required
        inputs.
        choices: [ocsp, user, client, ca, server]
        default: null
        type: str
```

## ENTRY POINT: sign - Sign certificate request

        This is generally the main task of a certificate authority,
        which is to issue signed certificates

### OPTIONS (= is mandatory):
```
= csr_text
        PEM-formatted certificate signing request
        type: str

- pki_home
        Top level directory where all CAs keep their home directories
        default: /srv/pki
        type: str

= purpose
        What purpose will the signed certificate be serving?
        Used to determine which extensions to add when issuing the
        cert
        choices: [ocsp, user, client, ca, server]
        type: str

= signing_ca
        Common Name of the certificate authority that will sign this
        certificate request
        type: str
```

## ENTRY POINT: root-ca - Manage Root Certificate Authority

        Create directory structure and files for managing a
        "lightweight" root Certificate Authority using openssl

### OPTIONS (= is mandatory):
```
- pk_passphrase
        Passphrase for the private key
        default: `input required if not provided'
        type: str

- pki_home
        Top level directory where all CAs keep their home directories
        default: /srv/pki
        type: str

- root_ca_cn
        Common Name for the root CA
        default: root-ca
        type: str

- root_ca_ou
        Organizational Unit for the Root CA
        default: Hermleigh Home Root CA
        type: str
```

### EXAMPLE

```
ansible $DEVICE_HOST -b -m include_role -a name=ca
```

## ENTRY POINT: sub-ca - Manage Intermediate (Subordinate) Certificate Authority

        Create directory structure and files for managing a
        "lightweight" Certificate Authority, subordinate to another CA

### OPTIONS (= is mandatory):
```
= ca_name
        Common Name (CN) for the CA (also used in directory and other
        naming conventions)
        type: str

= orgnizational_unit_name
        Organizational Unit (OU) name for the CA
        type: str

- pk_passphrase
        Passphrase for the private key
        default: `input requested'
        type: str

- pki_home
        Top level directory where all CAs keep their home directories
        default: /srv/pki
        type: str

= signing_ca
        Shortname of the certificate authority that will sign this
        certificate request
        type: str
```
