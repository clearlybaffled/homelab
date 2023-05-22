#!/bin/bash

HELM=/usr/local/bin/helm
JQ=/usr/bin/jq
VALUES=values.yaml
KONFIG=kustomization.yaml
YQ=/home/jared/bin/yq

$HELM install --create-namespace -f $VALUES $($YQ -o=json -I=0 '.helmCharts[0]' $KONFIG | $JQ -r --arg name $(basename $PWD) '"\($name) \(.name) --version \(.version) --repo \(.repo) -n \(if .namespace then .namespace else $name end) "')
