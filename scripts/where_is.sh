#!/usr/bin/env bash

if [ $# -ne 1 ]; then
    echo "Cloud name is required"
    exit 1
fi

CLOUD_NAME=$1

DNS=$(aws cloudformation describe-stacks --stack-name ${CLOUD_NAME}-cms --query 'Stacks[0].Outputs[0].OutputValue' --output text | awk '{print tolower($0)}')
echo "http://${DNS}"
