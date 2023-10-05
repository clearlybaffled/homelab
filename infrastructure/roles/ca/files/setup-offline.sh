#!/bin/bash -xe

# https://wiki.archlinux.org/title/Dm-crypt/Encrypting_an_entire_system#Plain_dm-crypt

# TODO: Figure out how to find device file from serial number
# if [ -n $1 ]; then
#   usb_device=$1
# else
#   echo "Need to provide a usb device"
#   exit 1
# fi


# Read private vars from stdin?
# like sops -d vars.yml | setup-offline.sh ?
# while IFS= read -r line; do
#   eval $line
# done < "${1:-/dev/stdin}"

lsblk=$(lsblk -dn -b -o SIZE,LOG-SEC $usb_device)
size=$lsblk[0] # bytes
bs=$lsblk[1] # bytes/block
crypt_name=pki
data_name=data
data_start=$(($crypt_offset + (($crypt_size+1)*1024*1024/$bs)))

#parted -s $usb_device mklabel gpt
#parted -s $usb_device mkpart $data_name ext4 ${data_start}s $(($key_offset - 1))s
#parted -s $usb_device print
#mkfs.ext4 ${usb_device}1


# https://wiki.archlinux.org/title/Dm-crypt/Device_encryption#Creating_a_keyfile_with_random_characters
 dd  \
  if=/dev/urandom  \
  of=$usb_device \
  bs=$bs \
  seek=$key_offset \
  count=$key_size \
  iflag=fullblock 


# https://wiki.archlinux.org/title/Dm-crypt/Device_encryption#Encryption_options_for_plain_mode
  cryptsetup open \
  --type plain \
  --size=$((crypt_size*1024*1024/$bs)) \
  --offset=$crypt_offset \
  --key-file=$usb_device \
  --keyfile-offset=$(($key_offset*$bs)) \
  --keyfile-size=$(($key_size*$bs)) \
  $usb_device \
  $crypt_name 

if [ -e /dev/mapper/$crypt_name ]; then
  mkfs.ext4 /dev/mapper/$crypt_name
  mount /dev/mapper/$name /srv/$name
fi
