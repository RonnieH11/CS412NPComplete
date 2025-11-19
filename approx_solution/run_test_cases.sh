#!/bin/bash

for file in test_cases/*.txt
do
    echo "Running test case: $file"
    python3 cs412_mingraphcoloring_approx.py < $file
    echo "Done with test case: $file"
done