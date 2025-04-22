#!/bin/bash

(gh auth status || gh auth login) && gh extension install https://github.com/nektos/gh-act

pip3 install --user pipreqs pytest flake8 auto8
pip3 install --user -r requirements.txt
