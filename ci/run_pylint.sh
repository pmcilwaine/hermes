#!/usr/bin/env bash

ROOT_DIR=$(dirname $0)/..
cd ${ROOT_DIR}

HAS_VIRTUAL_ENV=1

if [ -z "$VIRTUAL_ENV" ]; then
    HAS_VIRTUAL_ENV=0
    virtualenv pylint_env
    source pylint_env/bin/activate
    pip install pylint
fi

for i in hermes_aws hermes_cms; do
    pip install -r ${i}/requirements.txt
done

pylint --rcfile=${ROOT_DIR}/ci/pylintrc `git ls-tree --full-tree --name-only -r HEAD | egrep '\.py$' | egrep -v '/?tests/|/setup\.py|/local\.py|/hermes_cloud|stack_manager'` 2>&1 | tee pylint.log

if [ ${HAS_VIRTUAL_ENV} -eq 0 ]; then
    deactivate
fi
