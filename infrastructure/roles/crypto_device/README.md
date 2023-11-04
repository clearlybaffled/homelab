<!-- markdownlint-disable MD040 MD024 MD046 -->
# CRYPTO_DEVICE    (infrastructure/roles/crypto_device)

## ENTRY POINT: create

        Provision an encrypted section of a storage device

### OPTIONS (= is mandatory)

```
- crypt_device_file
        File name of the storage device to use. Not required if
        `serial_no' given.
        default: null

= crypt_key_file
        File name to use as the key file

= crypt_key_offset
        Sector number where the encryption key begins in the key file

- crypt_name
        Name used for the crypt
        default: pki

= crypt_offset
        Sector number to start the encrypted volume

= crypt_size
        Size (MiB) of the encrypted volume

= key_size
        Size (KiB) of the encryption key

- serial_no
        Serial number of the storage device to use for autodetection.
        default: null
```

## ENTRY POINT: open

        Opens an encrypted storage device

### OPTIONS (= is mandatory)

```
- crypt_device_file
        File name of the storage device to use. Not required if
        `serial_no' given.
        default: null

= crypt_key_file
        File name to use as the key file

= crypt_key_offset
        Sector number where the encryption key begins in the key file

- crypt_name
        Name used for the crypt
        default: pki

= crypt_offset
        Sector number to start the encrypted volume

= crypt_size
        Size (MiB) of the encrypted volume

= key_size
        Size (KiB) of the encryption key

- serial_no
        Serial number of the storage device to use for autodetection.
        default: null
```

### EXAMPLE

```
ansible $DEVICE_HOST -b -m include_role -a name=crypto_device -e cmd=open
```

## ENTRY POINT: close

        Closes an open encrypted storage device

### OPTIONS (= is mandatory)

```
- crypt_name
        Name used for the crypt
        default: pki

- mapping_file
        File created by `cryptsetup open' in "/dev/mapper
        default: /dev/mapper/{{ crypt_name }}
```

### EXAMPLE

```
ansible $DEVICE_HOST -b -m include_role -a name=crypto_device -e cmd=close
```

## ENTRY POINT: main

        Manage an encrypted storage device

### OPTIONS (= is mandatory)

```
= cmd
        Name of the task to execute
        choices: [create, open, close]
```
