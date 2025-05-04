#!/bin/bash

curl -fsSL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh -o install-scout.sh
sh install-scout.sh
rm -f install-scout.sh

(gh auth status || gh auth login) && gh extension install https://github.com/nektos/gh-act

pip3 install --user poetry pytest pytest-cov pytest-mock
poetry install --with test

npm ci
