#!/usr/bin/env bash

set -e

function help_text {

    cat <<EOF

    Usage: ci/integration_tests.sh [ -v|--version VERSION ] [ -c|--config CONFIGURATION ] [ -u|--url BASE_URL ]

        VERSION:        The RPM version to test against
        CONFIGURATION:  ci or local (defaults to ci)
        BASE_URL:       Location of server to run tests against

    Developer example:
        ci/integration_tests.sh -c ci

    CI example:
        ci/integration_tests.sh -v 201502191412

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
            export VERSION="$2"
            shift; shift
        ;;
        -c|--config)
            export CONFIGURATION="$2"
            shift; shift
        ;;
        -u|--url)
            export BASE_URL="$2"
            shift; shift
        ;;
        --username)
            export SAUCE_USER="$2"
            shift; shift
        ;;
        --key)
            export SAUCE_KEY="$2"
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
cd ${ROOT_DIR}/tests

export CONFIGURATION="${CONFIGURATION-ci}"
export TEST="e2e"

if [ -n  "${VERSION}" ]; then
    export BASE_URL="http://$(aws ec2 describe-instances --filter Name=tag:Name,Values=hermes_cms_${VERSION} | jq -r '.Reservations[0].Instances[0].PublicIpAddress')"
fi

attempts=1
until $(curl --output /dev/null --silent --get --fail ${BASE_URL}); do
    echo "Waiting for website to respond: ${BASE_URL}"
    if [ ${attempts} -gt 15 ]; then
        echo "Failed to contact website - make sure you are specifying the correct BASE_URL for the cloud"
        exit 1
    fi
    attempts=$((attempts+1))
    sleep 5
done

echo "OK"

npm test
status=$?
