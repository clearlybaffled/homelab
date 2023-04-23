#!/bin/bash

HELM=/usr/local/bin/helm
JQ=/usr/bin/jq
VALUES=values.yaml
CONFIG=config.js

$HELM install -f $VALUES $($JQ -r --arg name $(basename $PWD) '"\(.helm.chart) \($name) --version \(.helm.version) --repo \(.helm.repo) -n \(if .namespace then .namespace else $name end) "' <$CONFIG)
