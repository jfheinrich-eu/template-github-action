#!/bin/bash

(gh auth status || gh auth login) && gh extension install https://github.com/nektos/gh-act

pip3 install poetry
poetry install --with test

npm ci
