/*
    Tarefa A — Laço irregular e políticas de schedule

    Kernel: para i = 0..N-1, compute fib(i % K) e grave em v[i] usando fib custosa sem memoização.
    Variante 1: #pragma omp parallel for schedule(static)
    Variante 2: schedule(dynamic,chunk) com chunk ∈ {1,4,16,64}
    Variante 3: schedule(guided,chunk) com chunk ∈ {1,4,16,64}
    Se houver dois laços paralelos em sequência, use uma única região parallel e dois for internos  
*/


#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

typedef struct{
    int num_threads;
    int chunks;
    int N;
    int K;
} s_args;

s_args* get_args(int argc, char *argv[]){

    s_args *arguments = malloc(sizeof(s_args));

    if (argc != 5)
    {
        //printf("Usage: %s <num_threads> <N> <K> <chunks>\n", argv[0]);
        exit(1);
    } 
    else 
    {
        arguments->num_threads = atoi(argv[1]);
        arguments->N = atoi(argv[2]);
        arguments->K = atoi(argv[3]);
        arguments->chunks = atoi(argv[4]);
        
        if (arguments->num_threads <= 0 || arguments->N <= 0 || arguments->K <= 0 || arguments->chunks <= 0) {
            printf("All arguments must be positive integers!\n");
            exit(1);
        }
        
        //printf("Number of threads: %d, N: %d, K: %d, Chunks: %d\n", arguments->num_threads, arguments->N, arguments->K, arguments->chunks);
    }

    return arguments;

}

long fib(int n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
}

int main(int argc, char *argv[]) {
    s_args *args = get_args(argc,argv);
    long *v1 = malloc(args->N * sizeof(long));
    long *v2 = malloc(args->N * sizeof(long));
    long *v3 = malloc(args->N * sizeof(long));
    long *v4 = malloc(args->N * sizeof(long));

    omp_set_num_threads(args->num_threads);

    double start = omp_get_wtime();
    for (int i = 0; i < args->N; i++) { v1[i] = fib(i % args->K); }
    double end = omp_get_wtime();
    printf("sequential,%d,%d,%d,0,%.6f\n", args->num_threads, args->N, args->K, end - start);


    start = omp_get_wtime();
    #pragma omp parallel for schedule(static)
    for (int i = 0; i < args->N; i++) { v2[i] = fib(i % args->K); }
    end = omp_get_wtime();
    printf("static,%d,%d,%d,0,%.6f\n", args->num_threads, args->N, args->K, end - start);

    start = omp_get_wtime();
    #pragma omp parallel for schedule(dynamic, args->chunks)
    for (int i = 0; i < args->N; i++) { v3[i] = fib(i % args->K); }
    end = omp_get_wtime();
    printf("dynamic,%d,%d,%d,%d,%.6f\n", args->num_threads, args->N, args->K, args->chunks, end - start);

    start = omp_get_wtime();
    #pragma omp parallel for schedule(guided, args->chunks)
    for (int i = 0; i < args->N; i++) { v4[i] = fib(i % args->K);}
    end = omp_get_wtime();
    printf("guided,%d,%d,%d,%d,%.6f\n", args->num_threads, args->N, args->K, args->chunks, end - start);
    
    free(v1);
    free(v2);
    free(v3);
    free(v4);
    free(args);

    return EXIT_SUCCESS;
}