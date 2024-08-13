# Calibre

![Calibre logo](https://raw.githubusercontent.com/kovidgoyal/calibre/master/icons/calibre.png)

## Background

Up until [recently](https://github.com/clearlybaffled/homelab/blob/994d7e6815f83f2621c3ac29cb1948e5a3f736cc/cluster/apps/media/calibre/values.yaml), I had been deploying both calibre and calibre-web containers to one pod.
The thing was, the container from the nice folks at linuxserver.io didn't work very well for me.
It was based on running the Linux Calibre desktop app inside of kasm, a vnc like X server accessible from a browser. Sounds cool, but it would crash constantly.
Eventually, I would just use the calibre app on my Windows desktop to manage the catalog, and the only purpose for the containerized Calibre was to run the web server/opds server for remote book readers, like Moonreader.

This led me to think about trying to avoid running the full on kasm server and  learning that you could [run the calibre content server as a standalone executable](https://manual.calibre-ebook.com/server.html#integrating-the-calibre-content-server-into-other-servers),
I now had a way forward.

## Setup

First, I thought about trying to change the command or entry point to the calibre container to only start the server binary, but I got lost a few times digging through the
[several](https://github.com/linuxserver/docker-calibre/blob/master/Dockerfile)
[layers](https://github.com/linuxserver/docker-baseimage-kasmvnc/blob/master/Dockerfile)
[of](https://github.com/linuxserver/docker-baseimage-alpine-nginx/blob/master/Dockerfile) Dockerfiles that make up the whole image.

But then I realized that, through the [docker mod](https://mods.linuxserver.io/?mod=calibre-web) provided by linuxserver.io, calibre itself was *also* getting installed into the [calibre-web container](https://github.com/clearlybaffled/homelab/blob/736dc1332116e40e8dee6d129e5b58fe11a829fa/cluster/apps/media/calibre/values.yaml#L14).
So off I went!
I leaned all about how [s6]( https://skarnet.org/software/s6/index.html) works, wrote up an init container with some shared mounts and a ConfigMap. Five hours and one very frustrated wife later,
I had the calibre-server binary running directly in the calibre-web container, and no more Kasm!
