#!/usr/bin/env sh

set -xe

docker build $(dirname "$0")/.. -f $(dirname "$0")/Dockerfile -t pyconuk-2018-k8s:step2
