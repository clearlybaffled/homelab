provider "libvirt" {
  uri   = "qemu+ssh://ansible@parche/system?keyfile=$HOME/.ssh/ansible"
}