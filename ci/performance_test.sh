#!/usr/bin/env bash

while [ $# -gt 0 ]; do

    arg=$1

    case $arg in
        -h|--host)
            export HOST="$2"
            shift; shift
        ;;
        -p|--port)
            export PORT="$2"
            shift; shift
        ;;
        -v|--version)
            export VERSION="$2"
            shift; shift
        ;;
    esac
done

ROOT_DIR=$(readlink -m $(dirname $0)/..)
cd ${ROOT_DIR}

if [ ! -z ${VERSION} ]; then
    ELB_NAME=$(aws elb describe-load-balancers | grep -B 9 "hermes-ci" | grep "LoadBalancerName")
    ELB_NAME=${ELB_NAME:33:$((${#ELB_NAME} - 36))}

    HOST=$(aws elb describe-load-balancers --load-balancer-names ${ELB_NAME} --query 'LoadBalancerDescriptions[0].DNSName' --output text | tr '[:upper:]' '[:lower:]')
fi

export PORT=${PORT-80}
export HOST=${HOST-localhost}

curl --silent -O http://apache.mirror.serversaustralia.com.au/jmeter/binaries/apache-jmeter-2.13.tgz
tar -xzf apache-jmeter-2.13.tgz

echo "Running Test"
${ROOT_DIR}/apache-jmeter-2.13/bin/jmeter.sh -n -t ${ROOT_DIR}/tests/performance/performance-test.jmx -l ${ROOT_DIR}/tests/performance/results.jtl -Jsite=${HOST} -Jport=${PORT}
