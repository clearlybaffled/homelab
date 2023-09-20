terraform {
  required_providers {
    libvirt = {
      source = "dmacvicar/libvirt"
    }
  }
}

provider "libvirt" {
  uri   = "qemu+ssh://ansible@parche/system?keyfile=./ansible"
}