#!/usr/bin/env sh

set -xe

docker build $(dirname "$0")/.. -f step2/Dockerfile -t pyconuk-2018-k8s:step2
