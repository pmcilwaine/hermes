#!/usr/bin/env bash

if [ $# -lt 1 ]; then
    cat >&2 << EOF
Usage:
`basename $0` BUILD_VERSION
EOF
    exit 1
fi

ROOT_DIR=$(readlink -m $(dirname $0)/..)
BUILD_VERSION=$1
VERSION=$(cat ${ROOT_DIR}/core/VERSION)

cat ${ROOT_DIR}/README.md | tail -n+2 > ${ROOT_DIR}/tmpfile

cd ${ROOT_DIR}/docs
mkdir -p ${ROOT_DIR}/docs/output/developer
mkdir -p ${ROOT_DIR}/docs/output/userguide

# create developer documentation
#pandoc --template=templates/developer.html --variable=build:${BUILD_VERSION}

# get documents
DOCUMENTS=$(find developer -type f | xargs)
pandoc --template=templates/template.html -s ${ROOT_DIR}/tmpfile ${DOCUMENTS} \
    -o output/developer/index.html --variable=build:${BUILD_VERSION} \
    --variable=version:${VERSION} --variable=date:"$(date)" \
    --variable=doctype:"Developer Guide" --toc --highlight-style pygments


DOCUMENTS=$(find userguide -type f | xargs)
pandoc --template=templates/template.html ${ROOT_DIR}/tmpfile ${DOCUMENTS} \
    -o output/userguide/index.html --variable=build:${BUILD_VERSION} \
    --variable=version:${VERSION} --variable=date:"$(date)" \
    --variable=doctype:"User Guide" --toc

# pandoc -t latex ${ROOT_DIR}/tmpfile ${DOCUMENTS} \
#    -o output/userguide/index.latex --variable=build:${BUILD_VERSION} \
#    --variable=version:${VERSION} --variable=date:"$(date)" \
#    --variable=doctype:"User Guide" --toc

rm ${ROOT_DIR}/tmpfile

# create user guide documentation
#pandoc --template=templates/userguide.html --variable=build:${BUILD_VERSION}

# generate api documentation
#(cat ${ROOT_DIR}/ci/DoxygenFile; echo "PROJECT_NUMBER=${VERSION}") | doxygen -

# https://github.com/Velron/doxygen-bootstrapped
#HTML_HEADER =
#HTML_FOOTER =
#HTML_STYLESHEET =
#INPUT_FILTER = "python /path/to/doxypy.py"
#FILTER_SOURCE_FILES = YES
#HIDE_UNDOC_RELATIONS = NO
#OPTIMIZE_OUTPUT_JAVA = YES
#JAVADOC_AUTOBRIEF = YES
#MULTILINE_CPP_IS_BRIEF = YES
#DETAILS_AT_TOP = YES
#EXTRACT_ALL = YES
#EXTRACT_STATIC = YES
#SHOW_DIRECTORIES = YES
#SOURCE_BROWSER = YES
#ALPHABETICAL_INDEX = YES
#COLS_IN_ALPHA_INDEX = 8
#TOC_EXPAND = YES
#DISABLE_INDEX = YES
#GENERATE_TREEVIEW = YES
