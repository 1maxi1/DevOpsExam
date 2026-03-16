#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python not found: $PYTHON_BIN" >&2
  exit 1
fi

# Ensure pip exists inside the agent environment.
if ! "$PYTHON_BIN" -m pip --version >/dev/null 2>&1; then
  if "$PYTHON_BIN" -m ensurepip --upgrade >/dev/null 2>&1; then
    :
  else
    # Fallback: download get-pip.py using stdlib (no curl/wget required)
    "$PYTHON_BIN" - <<'PY'
import pathlib, urllib.request
url = "https://bootstrap.pypa.io/get-pip.py"
path = pathlib.Path("get-pip.py")
urllib.request.urlretrieve(url, path)
print(f"Downloaded {url} -> {path}")
PY
    "$PYTHON_BIN" get-pip.py
  fi
fi

"$PYTHON_BIN" -m pip install --upgrade pip
"$PYTHON_BIN" -m pip install -r requirements.txt

