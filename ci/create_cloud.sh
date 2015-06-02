#!/usr/bin/env bash

set -e

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

ROOT_DIR=$(readlink -m $(dirname $0)/..)

# get AMI
IMAGE_ID=$(aws ec2 describe-images --filters Name=name,Values=hermes_cms_${VERSION} | jq -r '.Images[0].ImageId')

INSTANCE_ID=$(aws ec2 run-instances --image-id ${IMAGE_ID} --key-name pmcilwaine-aws --iam-instance-profile Name=instance-role --count 1  --instance-type t2.micro --security-group-ids sg-73d24616 | jq -r ".Instances[0].InstanceId")

until [ `aws ec2 describe-instances --instance-ids ${INSTANCE_ID} | jq -r '.Reservations[0].Instances[0].State.Name'` == "running" ]; do
    echo "Waiting for instance to start up"
    sleep 10
done

aws ec2 create-tags --resource ${INSTANCE_ID} --tags Key=Name,Value=hermes_cms_${VERSION}
