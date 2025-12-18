#!/bin/bash

make clean
make

OUT_A="./results/results_A.csv"
OUT_B="./results/results_B.csv"


#HEADERS DO CSV
if [[ ! -e $OUT_A ]]; then
    echo "variant,threads,N,K,chunk,time" > $OUT_A
fi
if [[ ! -e $OUT_B ]]; then
    echo "threads,variant,N,B,time" > $OUT_B
fi

N_VALUES=(100000 500000 1000000)
K_VALUES=(20 24 28)
B_VALUES=(32 256 4096)
T_VALUES=(1 2 4 8 16)
C_VALUES=(1 4 16 64)
V_VALUES=(1 2 3)
RUNS=5

if [[ $1 == "A" || -z $1 ]]; then
    echo "Running Task A..."
    for N in "${N_VALUES[@]}"; do
        for K in "${K_VALUES[@]}"; do
            for T in "${T_VALUES[@]}"; do
                for C in "${C_VALUES[@]}"; do
                    echo "A: N=$N K=$K T=$T C=$C"
                    for r in $(seq 1 $RUNS); do
                        ./bin/taskA $T $N $K $C >> $OUT_A
                    done
                done
            done
        done
    done
fi
if [[ $1 == "B" || -z $1 ]]; then
    echo "Running Task B..."
    for T in "${T_VALUES[@]}"; do
        for V in "${V_VALUES[@]}"; do
            for N in "${N_VALUES[@]}"; do
                for B in "${B_VALUES[@]}"; do
                    echo "B: T=$T V=$V N=$N B=$B"
                    for r in $(seq 1 $RUNS); do
                        output=$(./bin/taskB random $T $V $N $B 2>/dev/null)
                        echo "$T,$V,$N,$B,$output" >> $OUT_B
                    done
                done
            done
        done
    done
fi

echo "Done: $OUT_A, $OUT_B"