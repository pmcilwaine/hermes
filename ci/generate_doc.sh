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
VERSION=$(cat hermes_ui/hermes_ui.spec | grep Version | cut -f9 -d ' ')

cat ${ROOT_DIR}/README.md | tail -n+2 > ${ROOT_DIR}/tmpfile

for PACKAGE in hermes_cms hermes_cloud hermes_aws; do
    python ${ROOT_DIR}/${PACKAGE}/setup.py install
done

cd ${ROOT_DIR}/docs
mkdir -p ${ROOT_DIR}/docs/output/developer
mkdir -p ${ROOT_DIR}/docs/output/pdf

pandoc --template=${ROOT_DIR}/docs/templates/main.html --variable=build:${BUILD_VERSION} \
    --variable=version:${VERSION} --toc --variable=date:"$(date)" \
    -s ${ROOT_DIR}/tmpfile -o ${ROOT_DIR}/docs/output/developer/index.html

for file in $(find ${ROOT_DIR}/docs/developer -name "*.md" -type f); do
    pandoc --template=${ROOT_DIR}/docs/templates/main.html --variable=build:${BUILD_VERSION} \
    --variable=version:${VERSION} --toc --variable=date:"$(date)" \
    -s ${file} -o ${ROOT_DIR}/docs/output/developer/$(basename ${file%%.*} | sed -e 's/[0-9_]//g').html
done

cp -R ${ROOT_DIR}/docs/developer/assets ${ROOT_DIR}/docs/output/developer/
cp -R ${ROOT_DIR}/docs/templates/css ${ROOT_DIR}/docs/output/developer/
cp -R ${ROOT_DIR}/docs/templates/js ${ROOT_DIR}/docs/output/developer/

cd ${ROOT_DIR}/docs/output/developer

echo "
import glob
from bs4 import BeautifulSoup

for filename in glob.glob('*.html'):
    soup = BeautifulSoup(open(filename, 'r').read(), 'html.parser')

    toc = soup.find(id='toc')
    toc_contents = BeautifulSoup(str(toc.findChild('ul').findChildren()[0]), 'html.parser')

    for ul_item in toc_contents.find_all('ul'):
        ul_item['class'] = 'nav nav-pills nav-stacked nav-list'

    toc.clear()

    toc.append(toc_contents)

    for table in soup.find_all('table'):
        table['class'] = 'table table-striped table-bordered'

    nav_item = soup.find('a', href=filename)
    if nav_item:
        nav_item.parent['class'] = 'active'

    open(filename, 'w').write(str(soup))
" | python -

# Developer PDF
cd ${ROOT_DIR}/docs/developer
pandoc -N --template=${ROOT_DIR}/docs/templates/template.tex \
    --variable=build:${BUILD_VERSION} --variable=title:"Hermes CMS" --variable=subtitle:"Developer Guide" \
    --variable version=${VERSION} $(find ${ROOT_DIR}/docs/developer -name "*.md" -type f) --toc \
    -o ${ROOT_DIR}/docs/output/pdf/Developer.pdf

# User Manual
cd ${ROOT_DIR}/docs/manual
pandoc -N --template=${ROOT_DIR}/docs/templates/template.tex \
    --variable=build:${BUILD_VERSION} --variable=title:"Hermes CMS" --variable=subtitle:"User Guide" \
    --variable version=${VERSION} $(find ${ROOT_DIR}/docs/manual -name "*.md" -type f) --toc \
    -o ${ROOT_DIR}/docs/output/pdf/UserManual.pdf

# generate api documentation
DOXYPY=$(which doxypy.py)
OUTPUT_DIRECTORY=${ROOT_DIR}/docs/api
INPUT_LIST="${ROOT_DIR}/README.md ${ROOT_DIR}/hermes_cms ${ROOT_DIR}/hermes_cloud ${ROOT_DIR}/hermes_aws"

(cat ${ROOT_DIR}/ci/DoxygenFile; cat << EOF
PROJECT_NUMBER=${VERSION}
INPUT_FILTER="python ${DOXYPY}"
INPUT=${INPUT_LIST}
OUTPUT_DIRECTORY="${OUTPUT_DIRECTORY}
EOF
) | doxygen -
