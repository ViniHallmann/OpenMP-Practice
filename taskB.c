#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <omp.h>

typedef struct{
    int num_threads;
    int test_num;
    int N;
    int B;
} s_args;

void print_help();
s_args* get_args(int argc, char *argv[]);
void histogram_critical(int *A, int N, int *H, int B);
void histogram_atomic(int *A, int N, int *H, int B);
void histogram_local(int *A, int N, int *H, int B);

int main(int argc, char *argv[])
{
    s_args *args = get_args(argc,argv);
    
    int *A = malloc(args->N * sizeof(int));
    int *H = calloc(args->B, sizeof(int));

    FILE *fptr;
    fptr = fopen("filename.txt", "r");

    if (fptr == NULL) {
        printf("Error: Could not open file. \n");
        printf("Want to use random data? (1 - yes) (2 - no)\n");
        printf(">: ");
        int select;
        scanf("%d",&select);
        if (select != 1){
            exit(1);
        } else {
            for(int i = 0; i < args->N; i++) A[i] = rand() % args->B; 
        }
    }else
        for (int i = 0; i < args->N; i++) fscanf(fptr, "%d", &A[i]);
   
    omp_set_num_threads(args->num_threads);
   
    double start = omp_get_wtime();

    if (args->test_num == 1) histogram_critical(A, args->N, H, args->B);
    else if (args->test_num == 2) histogram_atomic(A, args->N, H, args->B);
    else if (args->test_num == 3) histogram_local(A, args->N, H, args->B);
    
    double end = omp_get_wtime();
    printf("Time: %f\n", end - start);
     
    long total = 0;
    for (int i = 0; i < args->B; i++) total += H[i];
    printf("Total processed: %ld (expected: %d)\n", total, args->N);

    free(A);
    free(H);

    return EXIT_SUCCESS;
}

void print_help(){

    printf("Usage: ./taskB <file> <num-threads> <test-num> <N> <B>\n");
    printf("Tests numbers:\n");
    printf("1:\tUsing critical\n");
    printf("2:\tUsing atomic\n");
    printf("3:\tUsing local\n");
        
    exit(1);
}

s_args* get_args(int argc, char *argv[]){

    s_args *arguments = malloc(sizeof(s_args));

    if (argc != 6)
    {
        print_help();

    } else if (argc == 6 && 
    (isdigit((unsigned char)*argv[2]) == 0 || isdigit((unsigned char)*argv[3]) == 0 
    || isdigit((unsigned char)*argv[4]) == 0 || isdigit((unsigned char)*argv[5]) == 0 ))
    {
        printf("Some arguments must be numbers!\n");

        print_help();
    
    } else
    {
        arguments->num_threads = atoi(argv[2]); 
        arguments->test_num = atoi(argv[3]);
        if (arguments->num_threads < 0 || arguments->test_num > 3) print_help();
        
        arguments->N = atoi(argv[4]);
        arguments->B = atoi(argv[5]);
        
        printf("%d %d %d %d\n", arguments->num_threads, arguments->test_num, arguments->N, arguments->B);
    }

    return arguments;

}

void histogram_critical(int *A, int N, int *H, int B)
{
    #pragma omp parallel for
    for (int i = 0; i < N; i++) {
        int val = A[i];

        #pragma omp critical
        {
            H[val]++;
        }
    }
}

void histogram_atomic(int *A, int N, int *H, int B)
{
    #pragma omp parallel for
    for (int i = 0; i < N; i++) {
        int val = A[i];

        #pragma omp atomic    
        H[val]++;
        
    }
}

void histogram_local(int *A, int N, int *H, int B)
{
    #pragma omp parallel 
    {
        int *H_local = (int*) calloc(B, sizeof(int));

        #pragma omp for
        for (int i = 0; i < N; i++) {
            int val = A[i];
            H_local[val];
        }

        #pragma omp critical
        {
            for (int j = 0; j < B; j++) {
                H[j] += H_local[j];
            }
        }

        free(H_local);
    }
}