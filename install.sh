#!/usr/bin/env bash
set -e
################################################################
### Text automatically added by daps-utils calver-init ###
chmod +x .githooks/pre-commit
bash .githooks/pre-commit
ln -s $PWD/.githooks/pre-commit .git/hooks/pre-commit
################################################################
