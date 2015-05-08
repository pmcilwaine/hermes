#!/usr/bin/env bash

ROOT_DIR=$(dirname $0)/..
cd ${ROOT_DIR}

pylint --rcfile=${ROOT_DIR}/ci/pylintrc `git ls-tree --full-tree --name-only -r HEAD | egrep '\.py$' | egrep -v '/?tests/|/setup\.py|/local\.py'` 2>&1 | tee pylint.log
touch pylint.log

