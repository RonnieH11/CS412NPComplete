#!/usr/bin/env bash
# run_test_cases.sh
#
# Run the exact minimum graph coloring program on all .txt test cases
# in this directory. The driver lives one level up:
#   ../cs412_mingraphcoloring_exact.py
#
# NOTE: The test case "hard_long_runtime.txt" is intended to be the one
#       that runs for MORE THAN 20 MINUTES (tuned empirically).

set -euo pipefail

# Resolve paths relative to this script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROGRAM="${SCRIPT_DIR}/../cs412_mingraphcolor_exact.py"

if [ ! -f "$PROGRAM" ]; then
  echo "Error: cannot find driver program at $PROGRAM" >&2
  exit 1
fi

# Collect all .txt test files in this directory
shopt -s nullglob
TEST_FILES=("$SCRIPT_DIR"/*.txt)
shopt -u nullglob

if [ ${#TEST_FILES[@]} -eq 0 ]; then
  echo "No .txt test files found in ${SCRIPT_DIR}"
  exit 0
fi

for tc in "${TEST_FILES[@]}"; do
  # echo "=============================================="
  # echo "Running test case: $(basename "$tc")"

  if [[ "$(basename "$tc")" == "hard_long_runtime.txt" ]]; then
    echo "# NOTE: This test case is expected to run for MORE THAN 20 MINUTES."
  fi

  # Simple wall-clock timing using bash built-in
  start=$(date +%s)
  python3 "$PROGRAM" "$tc"
  end=$(date +%s)
  elapsed=$((end - start))

#   echo "Wall-clock time: ${elapsed} seconds"
#   echo
done
