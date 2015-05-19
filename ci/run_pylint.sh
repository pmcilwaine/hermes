#!/usr/bin/env bash

ROOT_DIR=$(dirname $0)/..
cd ${ROOT_DIR}

for i in hermes_aws hermes_cms; do
    if [ -z "$VIRTUAL_ENV" ]; then
        sudo pip install -r ${i}/requirements.txt
    else
        pip install -r ${i}/requirements.txt
    fi
done

pylint --rcfile=${ROOT_DIR}/ci/pylintrc `git ls-tree --full-tree --name-only -r HEAD | egrep '\.py$' | egrep -v '/?tests/|/setup\.py|/local\.py'` 2>&1 | tee pylint.log

