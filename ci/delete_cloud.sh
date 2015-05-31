#!/usr/bin/env bash

# this creates a single instance for now, everything is already configured

while [ $# -gt 0 ]; do

    arg=$1

    case $arg in

        -h|--help)
            help_text
        ;;
        -v|--version)
            export VERSION="$2"
            shift; shift
        ;;
        *)
            echo "ERROR: Unrecognised option: ${arg}"
            help_text
            exit 1
        ;;
    esac
done

INSTANCE_ID=$(aws ec2 describe-instances --filter Name=tag:Name,Values=hermes_cms_${VERSION} | jq -r '.Reservations[0].Instances[0].InstanceId')
aws ec2 terminate-instances --instance-ids ${INSTANCE_ID}
