# Reprodutibilidade do Experimento

## Ambiente de Software
* **Compilador:** Versao usada: `gcc-15`
* **OpenMP:** Versão suportada pelo compilador;
* **Python:** Versao usada: `3.13.2`
* **Bibliotecas Python:** `matplotlib`, `pandas`, `seaborn` (listadas em `requirements.txt`).

## 3. Como Executar
Passo a passo para compilar e rodar os testes:

1. **Instalar dependências (Python):**
   ```bash
   pip install -r requirements.txt

2. **Compilar:**
   ```bash
   make

3. **Executar**:
   ```bash
   chmod +x run.sh
   ./run.sh

4. **Gerar plots**:
    python3 src/plots/plotA.py
    python3 src/plots/plotB.py
