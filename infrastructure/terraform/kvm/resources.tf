resource "libvirt_volume" "fedora38-qcow2" {
  name   = "fedora38.qcow2"
  pool   = "cluster"
  source = "https://download.fedoraproject.org/pub/fedora/linux/releases/38/Cloud/x86_64/images/Fedora-Cloud-Base-38-1.6.x86_64.qcow2"
  format = "qcow2"
}
