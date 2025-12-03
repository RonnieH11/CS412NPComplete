#!/bin/bash

# Overwrite old results
echo "test_case,seconds" > runtimes.csv

for file in test_cases/*.txt
do
    echo "Running test case: $file"

    # Nanosecond timestamps
    start_ns=$(date +%s%N)
    python3 cs412_mingraphcolor_exact.py < "$file"
    end_ns=$(date +%s%N)

    # Elapsed time in nanoseconds
    elapsed_ns=$((end_ns - start_ns))

    # Convert to centiseconds (0.01s)
    elapsed_cs=$((elapsed_ns / 10000000))

    # Split into whole seconds and fractional part
    sec=$((elapsed_cs / 100))
    frac=$((elapsed_cs % 100))

    # Format as s.xx
    elapsed_str=$(printf "%d.%02d" "$sec" "$frac")

    echo "Runtime for $file: ${elapsed_str}s"
    echo "$(basename "$file"),$elapsed_str" >> runtimes.csv

    echo "Done with test case: $file"
done
