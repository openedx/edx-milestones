#!/usr/bin/env bash
set -e

export DJANGO_SETTINGS_MODULE=settings
echo 'Beginning Test Run...'
echo ''
echo 'Removing *.pyc files'
find . -name "*.pyc" -exec rm -rf {} \;

echo 'Running test suite'
coverage run manage.py test --verbosity=3
coverage report -m
coverage html
echo ''
echo 'View the full coverage report at {CODE_PATH}/edx-milestones/htmlcov/index.html'
echo ''
echo 'Testing Complete!'
