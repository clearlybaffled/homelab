#!/bin/bash

#docker-compose up --no-start
DOCKER_RUN="docker run -it --name ipa -h ipa.hermleigh.home -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v /srv/ipa/data:/data:Z --tmpfs /run --tmpfs /tmp -p 80:80 -p 443:443 -p 389:389 -p 636:636 -p 88:88 -p 464:464 -p 88:88/udp -p 464:464/udp --sysctl net.ipv6.conf.all.disable_ipv6=0 freeipa/freeipa-server:centos-8-4.8.7"

function optsfile {
  file="ipa-server-install-options.$1"
  if [ ! -f  $file ]; then
    >&2 echo "No such file $file" 
    exit 1
  fi

  sed -e "s/ADMIN_PASS/$ADMIN_PASS/" ipa-server-install-options.$1 | sed -e "s/DM_PASS/$DM_PASS/"   > ipa-server-install-options

  echo "Copying install options file to container"
  docker cp ipa-server-install-options ipa:/data
  rm ipa-server-install-options
}

#read -p "Enter Director Manager Password: " -s DM_PASS
#echo
#read -p "Enter IPA Admin Password: " -s ADMIN_PASS
#if [ -z $ADMIN_PASS ]
#then
#    ADMIN_PASS=$DM_PASS
#fi
#echo

#optsfile "external-ca"

echo "starting docker container"
#docker-compose up --no-recreate

$DOCKER_RUN ipa-server-install --external-ca --domain=hermleigh.home --realm=HERMLEIGH.HOME --ca-subject="CN=IPA Intermediate CA,O=HERMLEIGH.HOME,C=US" --subject-base="O=HERMLEIGH.HOME,C=US" --idstart=60001 --no-ntp

if [ $? -ne 0 ]; then
  exit 1
fi

echo "Get and sign the csr"
docker cp -L ipa:/root/ipa.csr ipa.csr

echo "Sign the csr"
read -n
sudo openssl ca -config /srv/pki/root-ca/root-ca.conf -extensions sub_ca_ext -out ipa.crt -infiles ipa.csr 

echo "Upload ipa cert, cacert, and continue install options"
docker cp ipa.crt ipa:/data
docker cp /srv/pki/root-ca/root-ca.crt ipa:/data/ca.crt

#optsfile "continue"

#docker-compose up --no-recreate
docker rm ipa
$DOCKER_RUN ipa-server-install --external-cert-file=/data/ca.crt --external-cert-file=/data/ipa.crt


