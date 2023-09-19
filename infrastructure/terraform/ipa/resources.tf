resource "libvirt_volume" "fedora38-qcow2" {
  name = "fedora38.qcow2"
  pool = "cluster" 
  source = "https://download.fedoraproject.org/pub/fedora/linux/releases/38/Cloud/x86_64/images/Fedora-Cloud-Base-38-1.6.x86_64.qcow2"
  format = "qcow2"
}

resource "libvirt_cloudinit_disk" "ipa-cloud-init" {
  name = "ipa-cloud-init.iso"
  pool = "cluster" 
  user_data      = file("${path.module}/ipa_cloud_init")
  network_config = file("${path.module}/ipa_network_config")
}

resource "libvirt_volume" "ipa-root" {
  name = "ipa-root.qcow2"
  pool = "cluster" 
  format = "qcow2"
  size = "10737418240"
  base_volume_id = "${libvirt_volume.fedora38-qcow2.id}"
}