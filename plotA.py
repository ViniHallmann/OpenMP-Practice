import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.figsize': (10, 6)})

def plot_taskA(df):
    os.makedirs("plots", exist_ok=True)
    
    df_main = df[df['N'] == 1000000].copy()
    
    print("Gerando gráfico de Escalabilidade...")
    plt.figure()
    
    # Filtramos: static, e dynamic/guided com chunk=64 (que vimos ser o melhor)
    # Se quiser ver todos, remova o filtro de chunk, mas o gráfico ficará cheio.
    subset = df_main[
        ((df_main['variant'] == 'static')) |
        ((df_main['variant'].isin(['dynamic', 'guided'])) & (df_main['chunk'] == 64)) |
        (df_main['variant'] == 'sequential')
    ]
    
    sns.lineplot(data=subset[subset['K'] == 28], x='threads', y='time', hue='variant', marker='o')
    plt.title('Escalabilidade: Tempo x Threads (N=1M, K=28)')
    plt.ylabel('Tempo (s)')
    plt.xlabel('Número de Threads')
    plt.savefig('plots/taskA_escalabilidade.png')
    plt.close()

    # 2. Comparação de Schedules (Barra)
    # Fixamos Threads=16 e K=28
    print("Gerando gráfico de Comparação de Schedules...")
    plt.figure()
    subset_bar = df_main[(df_main['threads'] == 16) & (df_main['K'] == 28)]
    
    # Cria uma coluna legível combinando Variante + Chunk
    subset_bar['Strategy'] = subset_bar.apply(lambda x: f"{x['variant']} (c={x['chunk']})", axis=1)
    
    sns.barplot(data=subset_bar, x='time', y='Strategy', hue='variant', errorbar='sd')
    plt.title('Comparação de Schedules (Threads=16, N=1M, K=28)')
    plt.xlabel('Tempo (s) - Menor é melhor')
    plt.savefig('plots/taskA_schedules.png')
    plt.close()

    # 3. Impacto do Chunk
    print("Gerando gráfico de Impacto do Chunk...")
    plt.figure()
    # Apenas dynamic e guided, threads=16, K=28
    subset_chunk = df_main[
        (df_main['variant'].isin(['dynamic', 'guided'])) & 
        (df_main['threads'] == 16) & 
        (df_main['K'] == 28)
    ]
    
    sns.lineplot(data=subset_chunk, x='chunk', y='time', hue='variant', marker='s')
    plt.xscale('log', base=2) # Escala log para os chunks 1, 4, 16, 64 ficarem espaçados
    plt.xticks([1, 4, 16, 64], labels=[1, 4, 16, 64])
    plt.title('Impacto do Tamanho do Chunk (Dynamic/Guided)')
    plt.ylabel('Tempo (s)')
    plt.xlabel('Tamanho do Chunk')
    plt.savefig('plots/taskA_chunks.png')
    plt.close()

if __name__ == "__main__":
    # Carrega dados
    try:
        df = pd.read_csv("results/results_A_RUN_3.csv")
        # Remove espaços em branco dos nomes das colunas
        df.columns = df.columns.str.strip()
        
        plot_taskA(df)
        print("Gráficos gerados na pasta 'plots/'!")
        
    except FileNotFoundError:
        print("Erro: Arquivo 'results/results_A_RUN_3.csv' não encontrado.")