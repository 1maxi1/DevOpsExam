#!/usr/bin/env bash
set -euo pipefail

bash ci/bootstrap_python.sh
.ci-venv/bin/python -m pytest

