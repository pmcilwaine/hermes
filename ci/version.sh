#!/usr/bin/env bash

ROOT_DIR=$(readlink -m $(dirname $0)/..)
export VERSION=`TZ='Australia/Sydney' date +%Y%m%d%H%M`
echo "VERSION=$VERSION" > ${ROOT_DIR}/version.properties
echo AMI Version: ${VERSION}
