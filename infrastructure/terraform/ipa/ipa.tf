resource "libvirt_domain" "ipa-server" {
  name       = "tang"
  memory     = "2048"
  vcpu       = 2
  autostart  = true
  qemu_agent = true


  network_interface {
    network_name = "virtnet"
  }

  disk {
    volume_id = libvirt_volume.ipa-root.id
    scsi      = true
  }

  cloudinit = libvirt_cloudinit_disk.ipa-cloud-init.id

  console {
    type        = "pty"
    target_type = "serial"
    target_port = "0"
  }

}
