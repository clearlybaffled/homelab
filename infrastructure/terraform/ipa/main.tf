terraform {
  required_version = ">= 1.6.0"
  required_providers {
    libvirt = {
      source  = "dmacvicar/libvirt"
      version = "0.7.1"
    }
    sops = {
      source  = "carlpett/sops"
      version = "1.0.0"
    }
  }
}
