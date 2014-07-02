#!/bin/bash
set -e
set -x

git config --global user.email "alice+travis@gothcandy.com"
git config --global user.name "Travis: Marrow"

travis_retry pip install --upgrade setuptools pytest
travis_retry pip install tox
travis_retry pip install python-coveralls
travis_retry pip install pytest-cov
