#!/bin/bash
make
echo "variant,threads,N,K,chunk,time" > results_test.csv

./bin/taskA 1 10000 15 1 >> results_test.csv
./bin/taskA 2 10000 15 1 >> results_test.csv
./bin/taskA 4 10000 15 1 >> results_test.csv
