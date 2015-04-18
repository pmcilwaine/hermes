#!/usr/bin/env bash
set -ex

function help_text {

    cat <<EOF
    Usage: ${0} [ -v|--version VERSION ] [ -b|--bucket BUCKET ]
        VERSION:        The RPM version to test against
        BUCKET:  	yum repo bucket (defaults to hermes-ci-paulmcilwaine-com)
    Developer example:
        ${0} -b  my-yum-bucket
    CI example:
        ${0} -v 201502191412
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
        -b|--bucket)
            export S3_BUCKET="$2"
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
export S3_BUCKET="${S3_BUCKET-hermes-ci-paulmcilwaine-com}"

cd ${ROOT_DIR}

mkdir -p ${ROOT_DIR}
aws s3 sync --delete s3://${S3_BUCKET}/ ${S3_BUCKET}
cp dist/*${VERSION}*.rpm ${S3_BUCKET}/
createrepo --update ${S3_BUCKET}
aws s3 sync --delete ${S3_BUCKET} s3://${S3_BUCKET}/
