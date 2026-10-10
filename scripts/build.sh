#!/usr/bin/env bash
# Build the pinned project with bounded Lake workers and one Lean thread per module.
set -euo pipefail
cd "$(dirname "$0")/.."
export LEAN_NUM_THREADS="${PAPER2_BUILD_THREADS:-2}"
if [[ ! "$LEAN_NUM_THREADS" =~ ^[1-9][0-9]*$ ]]; then
  echo "PAPER2_BUILD_THREADS must be a positive integer" >&2
  exit 2
fi
export MATHLIB_NO_CACHE_ON_UPDATE=1
unset LEAN_PATH LEAN_SRC_PATH
# Some macOS installations have Command Line Tools but an unconfigured Xcode.
if [[ "$(uname -s)" == Darwin && -d /Library/Developer/CommandLineTools ]]; then
  export DEVELOPER_DIR=/Library/Developer/CommandLineTools
  export PATH="/Library/Developer/CommandLineTools/usr/bin:$PATH"
fi
if [[ $# -eq 0 ]]; then
  set -- Paper2 Verification
fi
exec lake build "$@"
