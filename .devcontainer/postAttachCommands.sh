#!/bin/bash

(gh auth status || gh auth login) && gh extension install https://github.com/nektos/gh-act

pip3 install --user poetry pytest pytest-co pytest-mock
poetry install --with test

npm ci
