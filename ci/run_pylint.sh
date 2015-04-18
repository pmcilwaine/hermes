#!/usr/bin/env bash

ROOT_DIR=$(dirname $0)/..
cd ${ROOT_DIR}

# pylint --rcfile=${ROOT_DIR}/ci/pylintrc `find . -name "*.py" | egrep -v '/?tests/|/setup\.py'` 2>&1 | tee pylint.log
touch pylint.log

