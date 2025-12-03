#!/bin/bash

echo "Running time test"

for file in small_lightly_connected.txt small_highly_connected.txt non_optimal_test.txt
do
    echo Test case: $file
    echo Approx runtime:
    time python3 ../cs412_mingraphcolor_approx.py < $file > output.tmp
    colors=$(head -n 1 output.tmp)
    echo colors used $colors

    echo Exact runtime:
    time python3 ../../exact_solution/cs412_mingraphcolor_exact.py < $file > output.tmp
    colors=$(head -n 1 output.tmp)
    echo colors used $colors
done

for file in medium_lightly_connected.txt medium_highly_connected.txt
do
    echo Test case: $file
    echo Approx runtime:
    time python3 ../cs412_mingraphcolor_approx.py < $file > output.tmp
    colors=$(head -n 1 output.tmp)
done

for file in large_lightly_connected.txt large_highly_connected.txt
do
    echo Test case: $file
    echo Approx runtime:
    time python3 ../cs412_mingraphcolor_approx.py < $file > output.tmp
    colors=$(head -n 1 output.tmp)
    echo colors used $colors
done