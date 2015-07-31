#!/usr/bin/env bash

set -e

function help_text {

    cat <<EOF

    Usage: ${0} [ -v|--version VERSION ] [ -d|--domain DOMAIN ] [ -k|--key SSHKEY ] [ -n|--name NAME ]

        VERSION:        The RPM version to build
        SSHKEY:         The SSH Key to use to login and use for cloud
        NAME:           The name of the cloud to bring up.

EOF
    exit 1
}

[ $# -lt 3 ] && help_text

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
        -k|--key)
            export SSH_KEY="$2"
            shift; shift
        ;;
        -d|--domain)
            export DOMAIN="$2"
            shift; shift
        ;;
        -n|--name)
            export NAME="$2"
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

if [ ! -e ${SSH_KEY} ]; then
    exit 1
fi

NAME=${NAME-"hermes-ci-${VERSION}"}
SSH_KEY_NAME=$(basename ${SSH_KEY} .pem)
DELETE_CLOUD_SCRIPT="destroy_cloud -d ${DOMAIN} -n ${NAME} -r ap-southeast-2"
CREATE_IMAGE_ID=$(aws ec2 describe-images --filters Name=name,Values=hermes_cloud_${VERSION} | jq -r '.Images[0].ImageId')

echo "Getting instance..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id ${CREATE_IMAGE_ID} \
    --key-name ${SSH_KEY_NAME} \
    --instance-type t2.micro \
    --security-groups ssh-public \
    --count 1 \
    --iam-instance-profile Name=create-cloud | jq -r '.Instances[0].InstanceId')

echo "Waiting for instance..."
until [ `aws ec2 describe-instance-status --instance-ids ${INSTANCE_ID} | jq -r '.InstanceStatuses[0].SystemStatus.Status'` == "ok" ]; do
    sleep 10
done

IP_ADDRESS=$(aws ec2 describe-instances --instance-ids ${INSTANCE_ID} | jq -r '.Reservations[0].Instances[0].PublicIpAddress')

echo "Deleting Cloud..."
ssh -t -o StrictHostKeyChecking=no -i ${SSH_KEY} centos@${IP_ADDRESS} "${DELETE_CLOUD_SCRIPT}"

# take down create-cloud instance
echo "Taking down create_cloud instance"
aws ec2 terminate-instances --instance-ids ${INSTANCE_ID} > /dev/null
