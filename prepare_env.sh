#!/usr/bin/env bash

virtualenv env || exit 1
source env/bin/activate || exit 1

pip install -r pip-requirements.txt || exit 1