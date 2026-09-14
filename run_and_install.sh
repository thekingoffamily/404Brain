#!/usr/bin/env bash
# 404Brain — lazy install + run (Mac / Linux)
set -euo pipefail
cd "$(dirname "$0")"

echo
echo " ========================================"
echo "  404Brain — lazy install + run"
echo " ========================================"
echo

if [[ "$PWD" == *" "* ]]; then
  echo "[!] Path has SPACES. Move the repo to a path without spaces."
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "[!] Node.js not found. Install Node 20.18.2 then re-run."
  echo "    https://nodejs.org/"
  exit 1
fi

echo "[ok] Node $(node -v)  (want v20.18.2 — see .nvmrc)"
echo

if [[ ! -d node_modules ]]; then
  echo "[..] npm install  (first time = long)"
  npm install
else
  echo "[ok] node_modules already there — skip npm install"
  echo "     (rm -rf node_modules to force reinstall)"
fi
echo

export NODE_OPTIONS="${NODE_OPTIONS:---max-old-space-size=8192}"
echo "[..] npm run compile  (first time = several minutes)"
npm run compile
echo

if [[ ! -d src/vs/workbench/contrib/brain/browser/react/out ]]; then
  echo "[..] npm run buildreact"
  npm run buildreact || echo "[!] buildreact failed — continuing anyway"
else
  echo "[ok] react/out present — skip buildreact"
fi
echo

echo "[..] launching 404Brain..."
echo "     data: .tmp/user-data"
echo
exec ./scripts/code.sh --user-data-dir ./.tmp/user-data --extensions-dir ./.tmp/extensions "$@"
