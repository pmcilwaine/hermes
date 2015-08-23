#!/usr/bin/env bash

if [ $# -ne 2 ]; then
    echo "Cloud name is required"
    exit 1
fi

CLOUD_NAME=$1
SERVER_NAME=$2

ROOT_DIR=$(readlink -m $(dirname $0)/..)

if [ ! -e ${ROOT_DIR}/${CLOUD_NAME} ]; then

    if [ -z "$SSH_KEY" ]; then
        echo "Must set the SSH_KEY variable"
        exit 1
    fi

    NAT_IP=$(aws ec2 describe-instances --filters "Name=tag-value,Values=${CLOUD_NAME}-jumpbox-AZ1" --query 'Reservations[0].Instances[0].NetworkInterfaces[0].Association.PublicIp' --output text)
    CMS_IP=$(aws ec2 describe-instances --filters "Name=tag-value,Values=${CLOUD_NAME}-cms" --query 'Reservations[0].Instances[0].NetworkInterfaces[0].PrivateIpAddresses[0].PrivateIpAddress' --output text)
    LOG_IP=$(aws ec2 describe-instances --filters "Name=tag-value,Values=${CLOUD_NAME}-log" --query 'Reservations[0].Instances[0].NetworkInterfaces[0].PrivateIpAddresses[0].PrivateIpAddress' --output text)

    cat <<EOF > ${ROOT_DIR}/${CLOUD_NAME}
Host cms
    HostName ${CMS_IP}
    User centos
    ProxyCommand ssh -q ec2-user@${NAT_IP} -A nc %h %p
    IdentityFile ${SSH_KEY}
    StrictHostKeyChecking no

Host log
    HostName ${LOG_IP}
    User centos
    ProxyCommand ssh -q ec2-user@${NAT_IP} -A nc %h %p
    IdentityFile ${SSH_KEY}
    StrictHostKeyChecking no
EOF

fi

ssh -F ${ROOT_DIR}/${CLOUD_NAME} ${SERVER_NAME}
