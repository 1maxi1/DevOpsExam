#!/usr/bin/env bash
set -euo pipefail

bash ci/bootstrap_python.sh
python3 -m pytest

