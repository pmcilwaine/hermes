#!/usr/bin/env bash

set -xe

function help_text {

    cat <<EOF

    Usage: ${0} [ -v|--version VERSION ]

        VERSION:        The RPM version to build

EOF
    exit 1
}

[ $# -lt 1 ] && help_text


while [ $# -gt 0 ]; do

    arg=$1

    case $arg in

        -h|--help)
            help_text
        ;;
        -v|--version)
            export RELEASE="$2"
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
cd ${ROOT_DIR}

rm -f ${ROOT_DIR}/dist/*.rpm
mkdir -p ${ROOT_DIR}/dist

for i in hermes_cms; do
    python ${i}/setup.py bdist_rpm --release=${RELEASE}
    mv ${i}/dist/*.rpm ${ROOT_DIR}/dist/
done
