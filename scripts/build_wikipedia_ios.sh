#!/bin/bash
set -e

WORK_DIR=${PWD}
WIKIPEDIA_TMP_DIR=/tmp/wikipedia-ios

[[ -d ${WIKIPEDIA_TMP_DIR} ]] || git clone --depth=1 --single-branch https://github.com/wikimedia/wikipedia-ios.git ${WIKIPEDIA_TMP_DIR}
cd ${WIKIPEDIA_TMP_DIR}

cicd ios build --scheme Wikipedia --derived-data-path DerivedData
rm -rf ${WORK_DIR}/tmp/apps/Wikipedia.app
mkdir -p ${WORK_DIR}/tmp/apps
cp -r DerivedData/Build/Products/Debug-iphonesimulator/Wikipedia.app ${WORK_DIR}/tmp/apps/Wikipedia.app
