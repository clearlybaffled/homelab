#!/bin/bash
docker run -it --name ipa -h ipa.hermleigh.home  -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v /srv/ipa/data:/data:Z --tmpfs /run --tmpfs /tmp -p 80:80 -p 443:443 -p 389:389 -p 636:636 -p 88:88 -p 464:464 -p 88:88/udp -p 464:464/udp --sysctl net.ipv6.conf.all.disable_ipv6=0 freeipa/freeipa-server:centos-8-4.8.7 "$@"
