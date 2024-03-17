#!/bin/bash

HELM=/usr/local/bin/helm
JQ=/usr/bin/jq
VALUES=values.yaml
KONFIG=kustomization.yaml
YQ=/usr/local/bin/yq

# $HELM install --create-namespace -f $VALUES $($YQ -o=json -I=0 '.helmCharts[0]' $KONFIG | $JQ -r --arg name $(basename $PWD) '"\($name) \(.name) --version \(.version) --repo \(.repo) -n \(if .namespace then .namespace else $name end) "')

if [[ $# -ne 0 ]]; then
  pushd $1 &>/dev/null || return
fi

CMD="$HELM install --create-namespace -f $VALUES "
CMD+=$($YQ -o=json -I=0 '.helmCharts[0]' $KONFIG | $JQ -r --arg name $(basename $PWD) '"\($name) \(.name) --version \(.version) --repo \(.repo) -n \(if .namespace then .namespace else $name end) "')

echo "Command is: $CMD"

exec ${CMD}

popd &>/dev/null || true
