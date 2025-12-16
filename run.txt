#!/bin/bash

OUT=results_$1.csv
EXEC=./bin/task$1
FILE=$2

if [[ -z $FILE ]]; then
    FILE="random"
fi

n_values=(100000 500000 1000000)
k_values=(20 24 28)
b_values=(32 256 4096)
v_values=(1 2 3)
t_values=(1 2 4 8 16)

if [[ $1 == 'B' ]]; then
    echo "t,v,n,b,output" > "$OUT"

    for t in "${t_values[@]}"; do
        for v in "${v_values[@]}"; do
            for n in "${n_values[@]}"; do
                for b in "${b_values[@]}"; do

                    echo "Running: t=$t v=$v n=$n b=$b"

                    output=$($EXEC $FILE $t $v $n $b)

                    echo "$t,$v,$n,$b,$output" >> "$OUT"

                done
            done
        done
    done
fi