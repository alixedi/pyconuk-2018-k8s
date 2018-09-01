#!/usr/bin/env sh

set -xe

docker build $(dirname "$0")/provisioner -f $(dirname "$0")/provisioner/Dockerfile -t pyconuk-2018-k8s:provisioner
docker build $(dirname "$0")/webconsole -f $(dirname "$0")/webconsole/Dockerfile -t pyconuk-2018-k8s:webconsole
docker build $(dirname "$0")/consolehub -f $(dirname "$0")/consolehub/Dockerfile -t pyconuk-2018-k8s:consolehub-step4
