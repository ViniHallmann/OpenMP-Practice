import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

OUTPUT_DIR = "plots"

sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.figsize': (10, 6)})

def plot_escalability(df_main, K=28, N=1000000):
    plt.figure()
    subset = df[
        (df['N'] == N) & 
        (df['K'] == K) &
        (
            ((df['variant'] == 'static')) |
            ((df['variant'].isin(['dynamic', 'guided'])) & (df['chunk'] == 64)) |
            (df['variant'] == 'sequential')
        )
    ]
    
    if subset.empty: return

    sns.lineplot(data=subset, x='threads', y='time', hue='variant', marker='o')
    plt.title(f'Escalabilidade: Tempo x Threads (N={N}, K={K})')
    plt.ylabel('Tempo (s)')
    plt.xlabel('Número de Threads')
    plt.savefig(f'{OUTPUT_DIR}/taskA_escalabilidade_N{N}_K{K}.png')
    plt.close()

def plot_schedule_comparison(df_main, K=28, N=1000000, threads=16):
    plt.figure()
    subset_bar = df_main[(df_main['threads'] == threads) & (df_main['K'] == K) & (df_main['N'] == N)]
    if subset_bar.empty: return

    subset_bar['Strategy'] = subset_bar.apply(lambda x: f"{x['variant']} (c={x['chunk']})", axis=1)
    
    sns.barplot(data=subset_bar, x='time', y='Strategy', hue='variant', errorbar='sd')
    plt.title(f'Comparação de Schedules (Threads={threads}, N={N}, K={K})')
    plt.xlabel('Tempo (s)')
    plt.savefig(f'{OUTPUT_DIR}/taskA_schedules_N{N}_K{K}_threads{threads}.png')
    plt.close()

def plot_chunk_impact(df_main, K=28, N=1000000, threads=16):
    plt.figure()
    subset_chunk = df_main[
        (df_main['variant'].isin(['dynamic', 'guided'])) & 
        (df_main['threads'] == threads) & 
        (df_main['K'] == K) & 
        (df_main['N'] == N)
    ]

    if subset_chunk.empty: return
    
    sns.lineplot(data=subset_chunk, x='chunk', y='time', hue='variant', marker='s')
    plt.xscale('log', base=2)
    unique_chunks = sorted(subset_chunk['chunk'].unique())
    if unique_chunks: plt.xticks(unique_chunks, labels=unique_chunks)

    plt.title(f'Impacto do Tamanho do Chunk (Dynamic/Guided) - Threads={threads}, N={N}, K={K}')
    plt.ylabel('Tempo (s)')
    plt.xlabel('Tamanho do Chunk')
    plt.savefig(f'{OUTPUT_DIR}/taskA_chunks_N{N}_K{K}_threads{threads}.png')
    plt.close()

def plot_taskA(df):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    df_main = df[df['N'] == 1000000].copy()

    combinations = df[['N', 'K']].drop_duplicates().values
    
    for N, K in combinations:
        print(f"Gerando gráficos para N={N}, K={K} na pasta '{OUTPUT_DIR}'...")
        
        plot_escalability(df, K=K, N=N)
        
        available_threads = df[(df['N'] == N) & (df['K'] == K)]['threads'].unique()
        
        if len(available_threads) > 0:
            target_threads = 16 if 16 in available_threads else available_threads.max()
            
            plot_schedule_comparison(df, K=K, N=N, threads=target_threads)
            plot_chunk_impact(df, K=K, N=N, threads=target_threads)
    
    # print("Gerando gráfico de Escalabilidade...")
    # plot_escalability(df_main, K=28, N=1000000)


    # print("Gerando gráfico de Comparação de Schedules...")
    # plot_schedule_comparison(df_main, K=28, N=1000000, threads=16)

    # print("Gerando gráfico de Impacto do Chunk...")
    # plot_chunk_impact(df_main, K=28, N=1000000, threads=16)

if __name__ == "__main__":
    try:
        df = pd.read_csv("results/results_5_RUNS/results_A_RUN_5.csv")
        df.columns = df.columns.str.strip()
        
        plot_taskA(df)
        print("Gráficos gerados na pasta 'plots/'!")
        
    except FileNotFoundError:
        print("Erro: Arquivo 'results/results_A_RUN_3.csv' não encontrado.")