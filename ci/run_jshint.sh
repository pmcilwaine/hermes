#!/usr/bin/env bash

echo '<?xml version="1.0" encoding="utf-8"?><checkstyle version="4.3"></checkstyle>' > jshint.xml

ROOT_DIR=$(dirname $0)/..
cd ${ROOT_DIR}

cd hermes_ui

npm install
npm run jshint
