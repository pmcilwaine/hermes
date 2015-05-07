#!/usr/bin/env bash

ROOT_DIR=$(readlink -m $(dirname $0)/..)

cd ${ROOT_DIR}
${ROOT_DIR}/ci/version.sh

for module in $(find . -maxdepth 2 -name "tox.ini"); do
    tox -r -c ${module}
done
