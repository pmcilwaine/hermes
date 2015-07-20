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
cd ${ROOT_DIR}/baking

packer build -var version=${VERSION} -var base_ami=ami-f7740dcd -var image_name=hermes_cms one_role.json
packer build -var version=${VERSION} -var base_ami=ami-f7740dcd -var image_name=hermes_cloud one_role.json
