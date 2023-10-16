terraform {
  required_version = ">= 1.5.7"
  required_providers {
    libvirt = {
      source  = "dmacvicar/libvirt"
      version = "0.7.1"
    }
  }
}

provider "libvirt" {
  uri = "qemu+ssh://ansible@parche/system?keyfile=$HOME/.ssh/ansible"
}
