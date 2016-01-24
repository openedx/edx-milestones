#!/usr/bin/env bash
set -e

pep8 --config=.pep8 milestones
pylint --rcfile=.pylintrc milestones
