resource "libvirt_volume" "fedora38-qcow2" {
  name   = "fedora38.qcow2"
  pool   = "cluster"
  source = "https://download.fedoraproject.org/pub/fedora/linux/releases/38/Cloud/x86_64/images/Fedora-Cloud-Base-38-1.6.x86_64.qcow2"
  format = "qcow2"
}

resource "libvirt_network" "server_network" {
  name  = "servers"
  mode  = "bridge"
  bridge  = "br0"
}

resource "libvirt_network" "admin_network" {
  name = "admin"
  mode = "bridge"
  bridge = "br1"
}