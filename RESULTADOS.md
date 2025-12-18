# Resultados - Tarefa A - Fibonacci

## Informações:
- **N (Tamanho do Vetor):** Quantas vezes o loop vai rodar.
- **K (Custo/Irregularidade):** Define o quão "pesado" é o cálculo fib(i % K).
- **Schedules**
    - **Static:** (N iterações) em fatias iguais no início. Baixo overhead, mas se alguém pegar uma fatia "mais longa", os outros ficam esperando.
    - **Dynamic:** As threads pegam chunks sob demanda. Tem alto overhead.
    - **Guided:** Começa com fatias grandes e diminui. Tenta equilibrar os dois anteriores.

- **Cada ponto nos gráficos representa a média de 5 execuções.**

## Análise de Escalabilidade
Avaliamos o impacto do aumento de threads para o caso mais custoso ($N=1.000.000, K=28$).

![Escalabilidade](plots/5_RUNS/taskA_escalabilidade_N1000000_K28.png)

| Configuração | Tempo Médio (s) | Speedup |
|--------------|-----------------|---------|
| Sequencial   | 153.1s          | 1.0x    |
| 16 Threads   | 32.4s           | 4.7x    |

**Conclusão:** O algoritmo escala, reduzindo drasticamente o tempo de execução. O ganho não é perfeitamente linear devido ao overhead de gerenciamento das threads e limitações físicas dos núcleos da CPU.


## Comparação de Políticas de Escalonamento (Schedules)
Comparativo para $N=1.000.000, K=28$ com 16 Threads.

![Schedules](plots/5_RUNS/taskA_schedules_N1000000_K28_threads16.png)

| Schedule | Chunk | Tempo (s) | Análise |
|----------|-------|-----------|---------|
| **Static** | Auto  | **32.4s** | **Melhor Desempenho.** Baixo overhead e boa distribuição de carga devido. |
| Dynamic  | 1     | 39.9s     | Pior desempenho devido ao alto overhead de solicitar tarefas unitárias constantemente. |
| Guided   | 1     | 42.1s     | Desempenho intermediário/baixo, overhead inicial impacta. |

**Decisão:** Para este problema específico, onde a carga de trabalho pesada (`fib(28)`) se repete periodicamente, o escalonamento **Static** é a melhor escolha. O `Dynamic` adiciona custo de sincronização desnecessário, pois a carga já se encontra balanceada probabilisticamente em vetores grandes.

## Impacto do Chunk Size
Variando o chunk no escalonamento Dynamic ($N=1.000.000, K=28$).

![Chunk](plots/5_RUNS/taskA_chunks_N1000000_K28_threads16.png)

- **Chunk 1:** ~39.9s (Maior overhead)
- **Chunk 64:** ~39.4s (Menor overhead)

**Conclusão:** Observou-se uma anomalia de desempenho com chunk=16 no schedule Dynamic, que apresentou o pior tempo (~43.6s), superando até mesmo o overhead excessivo do chunk=1. O tamanho 16 causou uma distribuição desigual onde certas tarefas concentraram desproporcionalmente os cálculos pesados, anulando o benefício do balanceamento dinâmico