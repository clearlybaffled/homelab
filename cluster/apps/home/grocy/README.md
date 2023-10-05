# ![](https://raw.githubusercontent.com/grocy/grocy/master/public/img/logo.svg)

The first app I deployed to the cluster. I decided to try to build this one completely from scratch (i.e. without using [Bern's chart template](https://bjw-s.github.io/helm-charts/docs/app-template/introduction.html))
and used John Hamelinks's k8s-config's for [grocy](https://git.sr.ht/~johnhamelink/k8s-grocy/) and [barcode-buddy](https://git.sr.ht/~johnhamelink/k8s-barcodebuddy).
Currently, I've just configured each manifest file to have 2 YAML documents, one for each grocy and barcode-buddy.
My thoughts are, if I'm feeling enterprising enough, would be to reconfig it to have barcode-buddy run as a sidecar to grocy isntead of a separate pod, and maybe even share underlying volumes.
Grocy was also built and deployed before the [rook-ceph](../../infrastructure/rook-ceph/) storage solution was in place, so it uses local volumes (see [#22](https://github.com/clearlybaffled/homelab/issues/22) and [#23](https://github.com/clearlybaffled/homelab/issues/23)).
