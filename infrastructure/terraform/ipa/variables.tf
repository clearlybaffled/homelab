data "sops_file" "ansible_ssh_key" {
  source_file = "${path.module}/../../inventory/group_vars/all/ansible_user.sops.yml"
}

data "sops_file" "root_ca_crt" {
  source_file = "${path.module}/../../inventory/group_vars/all/pki/root-ca.sops.yml"
}

output "hosts_created" {
  value = [libvirt_domain.ipa-server.name]
}
