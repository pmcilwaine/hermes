#!/usr/bin/env bash

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

export CONFIGURATION="${CONFIGURATION-ci}" # Defaults to running on browserstack
export TEST="integration"

export CONFIGURATION="ci" # "local"
export BASE_URL="${BASE_URL-http://localhost:3000/}"

ROOT_DIR=$(readlink -m $(dirname $0)/..)
cd ${ROOT_DIR}/hermes_ui
npm install
npm run build

cd ${ROOT_DIR}/tests

# setup environment
npm install

until $(bash -c "echo > /dev/tcp/localhost/3000" 2> /dev/null); do
    echo "Starting browsersync webserver"
    npm run start &
    SERVER_PID=$!
    echo "Current PID is ${SERVER_PID}"
    sleep 20
done

# Run the web driver and wait for it to come up
if [ "${CONFIGURATION}" == "local" ]; then
    npm run webdriver > webdriver-debug.log &
    while ! timeout 1 bash -c "echo > /dev/tcp/localhost/4444"; do sleep 1; done
else    
    # ci and install sauce connect
    if [ $(uname) == "Darwin" ]; then
        curl https://saucelabs.com/downloads/sc-4.3.8-osx.zip -o sc-4.3.zip --silent
        unzip sc-4.3.zip
        mv sc-4.3.8-osx sc
    elif [ $(uname) == "Linux" ]; then
        curl https://saucelabs.com/downloads/sc-4.3.8-linux.tar.gz -o sc-4.3.tar.gz --silent
        tar -zxvf sc-4.3.tar.gz
        mv sc-4.3.8-linux sc
    else
        echo "Unknown operating system"
        exit 1
    fi

    # start sauce labs connect
    ./sc/bin/sc -u ${SAUCE_USER} -k ${SAUCE_KEY} --readyfile sauce.out > /dev/null &
    SAUCE_PID=$!

    attempts=1
    until [ -f "sauce.out" ]; do
        if [ ${attempts} -gt 15 ]; then
            echo "Cannot connect to sauce connect"
            exit 1
        fi

        echo "Waiting for sauce connect to be ready"
        sleep 10
        attempts=$((attempts+1))
    done

fi

npm test
status=$?

# Kill the web-driver server
if [ "${CONFIGURATION}" == "local" ]; then
    curl http://localhost:4444/selenium-server/driver/?cmd=shutDownSeleniumServer > /dev/null
fi

if [ ! -z ${SERVER_PID} ]; then
    kill ${SERVER_PID}
fi

# kill sauce connect
if [ ! -z ${SAUCE_PID} ]; then
    kill ${SAUCE_PID}
fi

exit ${status}
