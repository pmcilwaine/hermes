#!/usr/bin/env bash

ROOT_DIR=$(readlink -m $(dirname $0)/..)

cd ${ROOT_DIR}
${ROOT_DIR}/ci/version.sh

