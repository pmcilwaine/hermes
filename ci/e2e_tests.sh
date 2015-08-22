#!/usr/bin/env bash

set -e

function help_text {

    cat <<EOF

    Usage: ci/e2e_tests.sh [ -v|--version VERSION ] [ -c|--config CONFIGURATION ] [ -u|--url BASE_URL ]

        VERSION:        The RPM version to test against
        CONFIGURATION:  ci or local (defaults to ci)
        BASE_URL:       Location of server to run tests against

    Developer example:
        ci/e2e_test.sh -c ci

    CI example:
        ci/e2e_test.sh -v 201502191412

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

# setup environment
npm install

mkdir -p ${ROOT_DIR}/tests/e2e/files
# Download files so we can test
curl --silent https://s3-ap-southeast-2.amazonaws.com/tests-paulmcilwaine-com/test-service.txt -o ${ROOT_DIR}/tests/e2e/files/test-service.txt


export CONFIGURATION="${CONFIGURATION-ci}"
export TEST="e2e"

if [ -z "${BASE_URL}" ]; then
    ELB_NAME=$(aws elb describe-load-balancers | grep -B 9 "hermes-ci" | grep "LoadBalancerName")
    ELB_NAME=${ELB_NAME:33:$((${#ELB_NAME} - 36))}

    attempts=1
    until aws elb describe-instance-health --load-balancer-name ${ELB_NAME} | grep InService; do
        echo "Waiting for ${ELB_NAME} to respond"
        sleep 30
        if [ $attempts -gt 10 ]; then
            echo "${ELB_NAME} Failed health check"
            exit 1
        fi
        attempts=$((attempts+1))
    done

    BASE_URL=$(aws elb describe-load-balancers --load-balancer-names ${ELB_NAME} | jq -r '.LoadBalancerDescriptions[0].DNSName' | tr '[:upper:]' '[:lower:]')
    export BASE_URL="http://${BASE_URL}"
fi

export BASE_URL=$(echo ${BASE_URL} | awk '{print tolower($0)}')

attempts=1
until $(curl --output /dev/null --silent --head --fail --insecure ${BASE_URL}/login); do
    echo "Waiting for website to respond: ${BASE_URL}"
    sleep 5
    if [ $attempts -gt 15 ]; then
        echo "Failed to contact website - make sure you are specifying the correct BASE_URL if using a dev cloud"
        exit 1
    else
        attempts=$((attempts+1))
    fi
done

if [ "${CONFIGURATION}" = local ]; then
    npm run webdriver 2> webdriver-debug.log &
    while ! timeout 1 bash -c "echo > /dev/tcp/localhost/4444"; do sleep 1; done
fi

npm test
status=$?

# Kill the web-driver server
if [ "${CONFIGURATION}" == "local" ]; then
    curl http://localhost:4444/selenium-server/driver/?cmd=shutDownSeleniumServer > /dev/null
fi

exit ${status}
