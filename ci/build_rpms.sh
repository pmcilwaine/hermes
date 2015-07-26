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

for i in hermes_cloud hermes_cms hermes_aws; do
    python ${i}/setup.py bdist_rpm --release=${RELEASE}
    mv ${i}/dist/*.rpm ${ROOT_DIR}/dist/
done

# setup frontend ui rpm
cd ${ROOT_DIR}/hermes_ui
npm install
npm run build
mkdir -p rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
sed "s/{IMAGE_VERSION}/${RELEASE}/g" hermes_ui.spec > rpmbuild/SPECS/hermes_ui.spec
FOLDER_NAME=$(cat hermes_ui.spec | grep Name | awk '{ print $2 }')-$(cat hermes_ui.spec | grep Version | awk '{ print $2 }')
cp -R dist/ ${FOLDER_NAME}
tar -cvf rpmbuild/SOURCES/$(cat hermes_ui.spec | grep Name | awk '{ print $2 }')-$(cat hermes_ui.spec | grep Version | awk '{ print $2 }')-${RELEASE}.tar.gz ${FOLDER_NAME}
rpmbuild --define "_topdir ${PWD}/rpmbuild" -ba rpmbuild/SPECS/hermes_ui.spec
mv rpmbuild/RPMS/noarch/*.rpm ${ROOT_DIR}/dist/
