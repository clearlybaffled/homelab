#!/bin/bash

scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${scriptDir}/.." || exit 1
base=$(pwd)

if [ $# -ne 0 ]
then

  for repo in "$@"
  do
    path=$(dirname $repo)
    git clone --single-repo https://github.com/$repo $base/references/$path
  done

else

  for repo in $(ls $base/references)
  do
    git -C references/$repo pull --rebase
  done

fi
