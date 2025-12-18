import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# --- CONFIGURAÇÕES ---
ARQUIVO_CSV = './results/results_B.csv'
N_FIXO = 100000   # Ajuste para o N que quer analisar
B_FIXO = 32       # Ajuste para o B que quer analisar

# Mapa para nomes legíveis
MAPA_VARIANTES = { 1: 'Critical', 2: 'Atomic', 3: 'Local' }

sns.set_theme(style="whitegrid")

def carregar_dados():
    try:
        df = pd.read_csv(ARQUIVO_CSV)
        
        if df['time'].dtype == object:
            df['time'] = df['time'].str.replace(' s', '', regex=False)
        
        df['time_kernel'] = df['time'].astype(float)
        
        # Converte para Milissegundos (ms) para melhor leitura
        df['time_ms'] = df['time_kernel'] * 1000
        
        df['Metodo'] = df['variant'].map(MAPA_VARIANTES)
        return df
    except Exception as e:
        print(f"Erro ao ler CSV: {e}")
        exit()

# GRÁFICO 1: Tempo dos Kernels (Evolução)
def plot_tempo_kernels(df):
    plt.figure(figsize=(10, 6))
    
    # Gráfico de Linha com Desvio Padrão
    g = sns.lineplot(
        data=df, 
        x='threads', 
        y='time_ms', 
        hue='Metodo', 
        style='Metodo', 
        markers=True, 
        dashes=False,
        errorbar='sd',     # Desvio Padrão (sombra ou barra)
        err_style='bars',  # Barra vertical de erro
        err_kws={'capsize': 5},
        linewidth=2.5
    )
    
    # ESCALA LOGARÍTMICA (Obrigatória para ver Critical e Local juntos)
    g.set_yscale("log")
    g.yaxis.set_major_formatter(ticker.ScalarFormatter()) # Remove notação 10^x
    
    plt.title(f'1. Tempo de Execução dos Kernels (N={N_FIXO}, B={B_FIXO})', fontsize=14)
    plt.ylabel('Tempo (ms) - Escala Log', fontsize=12)
    plt.xlabel('Número de Threads', fontsize=12)
    plt.xticks(sorted(df['threads'].unique()))
    plt.legend()
    plt.grid(True, which="minor", ls="--", linewidth=0.3)
    
    plt.savefig('./plots/taskB_tempo_kernels.png')
    print("Salvo: ./plots/taskB_tempo_kernels.png ")
    plt.close()

# GRÁFICO 2: Escalabilidade (Speedup)
def plot_escalabilidade(df):
    plt.figure(figsize=(10, 6))
    
    # Calcula Speedup (Base: Média do Local com 1 Thread)
    # Se não tiver Local, tenta pegar qualquer um com 1 thread
    df_speedup = df.copy()
    
    base_filter = (df['Metodo'] == 'Local') & (df['threads'] == 1)
    if base_filter.sum() == 0:
        base_filter = (df['threads'] == 1)
        
    tempo_base = df[base_filter]['time_kernel'].mean()
    
    df_speedup['Speedup'] = tempo_base / df_speedup['time_kernel']
    
    sns.lineplot(
        data=df_speedup, x='threads', y='Speedup', hue='Metodo', style='Metodo',
        markers=True, dashes=False, errorbar=None, linewidth=2.5
    )
    
    # Linha Ideal
    max_threads = df['threads'].max()
    plt.plot([1, max_threads], [1, max_threads], '--', color='gray', label='Ideal', alpha=0.5)
    
    max_real_y = df_speedup['Speedup'].max()
    limite_y = max(1.5, max_real_y* 1.1)
    plt.ylim(0, limite_y)

    plt.title(f'2. Escalabilidade (Speedup) (N={N_FIXO}, B={B_FIXO})', fontsize=14)
    plt.ylabel('Speedup (x vezes)', fontsize=12)
    plt.xlabel('Threads', fontsize=12)
    plt.xticks(sorted(df['threads'].unique()))
    plt.legend()
    
    plt.savefig('./plots/taskB_escalabilidade.png')
    print("Salvo: ./plots/taskB_escalabilidade.png")
    plt.close()

# GRÁFICO 3: Comparativo Critical vs Atomic vs Local (Snapshot Barras)
def plot_comparativo_final(df):
    plt.figure(figsize=(10, 6))
    
    # Vamos pegar apenas o cenário com o MÁXIMO de threads para comparar o resultado final
    max_threads = df['threads'].max()
    df_max = df[df['threads'] == max_threads]
    
    # Barplot simples
    g = sns.barplot(
        data=df_max,
        x='Metodo',
        y='time_ms',
        hue='Metodo',
        errorbar='sd',
        capsize=.1,
        edgecolor=".2"
    )
    
    # Escala Log nas barras também, pois a diferença é brutal
    g.set_yscale("log")
    g.yaxis.set_major_formatter(ticker.ScalarFormatter())
    
    # Adicionar os valores em cima das barras para facilitar a leitura
    for container in g.containers:
        g.bar_label(container, fmt='%.2f ms', padding=3)

    plt.title(f'3. Comparativo Final com {max_threads} Threads (N={N_FIXO}, B={B_FIXO})', fontsize=14)
    plt.ylabel('Tempo (ms) - Escala Log', fontsize=12)
    plt.xlabel('Estratégia', fontsize=12)
    
    plt.savefig('./plots/taskB_variantes.png')
    print("Salvo: ./plots/taskB_variantes.png")
    plt.close()

# --- MAIN ---
if __name__ == "__main__":
    df = carregar_dados()
    
    # Filtra o cenário específico
    df_cenario = df[(df['N'] == N_FIXO) & (df['B'] == B_FIXO)].copy()
    
    if not df_cenario.empty:
        plot_tempo_kernels(df_cenario)
        plot_escalabilidade(df_cenario)
        plot_comparativo_final(df_cenario)
    else:
        print(f"Dados não encontrados para N={N_FIXO} e B={B_FIXO}.")