TEST_DIR="test_cases"

PYTHON_SCRIPT="cs412_mingraphcoloring_augment.py"

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: Python script $PYTHON_SCRIPT not found!"
    exit 1
fi

for file in "$TEST_DIR"/*.txt; do
    [ -e "$file" ] || continue

    echo "Running test case: $file"
    python3 "$PYTHON_SCRIPT" < "$file"
    echo "Done with test case: $file"
    echo
done
