# IPA

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.5.7 |
| <a name="requirement_libvirt"></a> [libvirt](#requirement\_libvirt) | 0.7.1 |
| <a name="requirement_sops"></a> [sops](#requirement\_sops) | 1.0.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_libvirt"></a> [libvirt](#provider\_libvirt) | 0.7.1 |
| <a name="provider_sops"></a> [sops](#provider\_sops) | 1.0.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [libvirt_cloudinit_disk.ipa-cloud-init](https://registry.terraform.io/providers/dmacvicar/libvirt/0.7.1/docs/resources/cloudinit_disk) | resource |
| [libvirt_domain.ipa-server](https://registry.terraform.io/providers/dmacvicar/libvirt/0.7.1/docs/resources/domain) | resource |
| [libvirt_volume.ipa-root](https://registry.terraform.io/providers/dmacvicar/libvirt/0.7.1/docs/resources/volume) | resource |
| [sops_file.ansible_ssh_key](https://registry.terraform.io/providers/carlpett/sops/1.0.0/docs/data-sources/file) | data source |
| [sops_file.root_ca_crt](https://registry.terraform.io/providers/carlpett/sops/1.0.0/docs/data-sources/file) | data source |

## Inputs

No inputs.

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_hosts_created"></a> [hosts\_created](#output\_hosts\_created) | n/a |
