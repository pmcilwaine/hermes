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

finish () {
    rv=$?
    if [ ${rv} -ne 0 ]; then

        for image_name in hermes_cloud hermes_cms; do
            IMAGE_ID=$(aws ec2 describe-images --filters Name=name,Values=${image_name}_${VERSION} | jq -r '.Images[0].ImageId')
            if [ "{$IMAGE_ID}" = "null" ]; then
                aws ec2 deregister-image --image-id ${IMAGE_ID}
            fi
        done
    fi
}

trap "finish" INT TERM EXIT

ROOT_DIR=$(readlink -m $(dirname $0)/..)
cd ${ROOT_DIR}/baking

for image_name in hermes_cms hermes_cloud; do
    packer build -var version=${VERSION} -var base_ami=ami-f7740dcd -var image_name=${image_name} one_role.json
done
