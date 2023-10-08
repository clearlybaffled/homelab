#!/bin/bash

scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "${scriptDir}/.." || exit 1
base=$(pwd)

if [ $# -ne 0 ]; then

	for repo in "$@"; do
		path=$(dirname $repo)
		git clone --single-branch https://github.com/$repo $base/references/$path
	done

else

	for repo in $base/references/*; do
		git -C $repo pull --rebase
	done

fi
