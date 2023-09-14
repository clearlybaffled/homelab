terraform {
  required_providers {
    libvirt = {
      source = "dmacvicar/libvirt"
    }
  }
}

provider "libvirt" {
  ## Configuration options
  #uri = "qemu:///system"
  #alias = "server2"
  uri   = "qemu+ssh://ansible@parche/system?keyfile=~/.ssh/ansible"
}

resource "libvirt_network" "virtnet" {
  name = "virtnet"
  domain = "hermleigh.home"
  mode = "bridge"
 
}