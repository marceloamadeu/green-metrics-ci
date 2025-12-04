# Green Metrics CI - Experimento de Consumo Energético

Estudo experimental sobre o impacto energético de estratégias de otimização de testes em pipelines de Integração Contínua.

## 📋 Estrutura do Projeto

```
green-metrics-ci/
├── src/
│   ├── __init__.py
│   ├── app.py           # Código-fonte com funções de teste
│   └── test_app.py      # Suíte de testes
├── scripts/
│   ├── orchestrator.py  # Orquestra 10 repetições dos experimentos
│   ├── metrics.py       # Análise estatística e visualizações
│   └── setup_runner.sh  # Prepara o ambiente do runner
├── .github/workflows/
│   ├── baseline.yml     # Execução sequencial
│   ├── parallel.yml     # Execução paralela com xdist
│   └── tia.yml          # Test Impact Analysis com testmon
├── data/
│   ├── raw/             # Artifacts baixados do GitHub
│   └── plots/           # Gráficos gerados
├── requirements.txt
└── README.md
```

## 🚀 Passo a Passo para Executar o Experimento

### 1. Configurar Self-Hosted Runner

**No GitHub:**
1. Vá para Settings → Actions → Runners → New self-hosted runner
2. Siga as instruções para instalar o runner na sua máquina Linux

**Na sua máquina:**
```bash
# Executar o script de setup
chmod +x scripts/setup_runner.sh
./scripts/setup_runner.sh

# Iniciar o runner
cd actions-runner
./run.sh
```

### 2. Executar os Experimentos

```bash
# Instalar dependências locais
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Rodar orquestrador (dispara 30 workflows automaticamente)
python3 scripts/orchestrator.py
```

**⏱️ Tempo estimado:** ~2 horas (30 execuções × ~3 min cada + cooldown)

### 3. Baixar os Resultados

Após todas as execuções concluírem no GitHub Actions:

```bash
# Listar as últimas 30 execuções
gh run list --limit 30

# Baixar artifacts de cada run
mkdir -p data/raw
for run_id in $(gh run list --json databaseId --limit 30 --jq '.[].databaseId'); do
    gh run download $run_id --dir data/raw/run-$run_id
done
```

### 4. Analisar os Dados

```bash
# Processar métricas e gerar gráficos
python3 scripts/metrics.py
```

**Saídas:**
- `data/resultados_consolidados.csv` - Dados tabulados
- `data/plots/*.png` - Gráficos para o artigo
- Testes de hipótese no terminal

## 📊 Métricas Coletadas

| Métrica | Unidade | Fonte |
|---------|---------|-------|
| Consumo de Energia | Joules (J) | Eco-CI |
| Tempo de Execução | Segundos (s) | pytest + Eco-CI |
| Emissões de CO2 | Gramas (g) | Eco-CI |
| EDP (Energy-Delay Product) | J·s | Calculado |
| Utilização de CPU | Porcentagem (%) | Eco-CI |
| Cobertura de Código | Porcentagem (%) | pytest-cov |

## 🧪 Tratamentos Experimentais

### Baseline (Sequencial)
- **Comando:** `pytest src/test_app.py`
- **Descrição:** Execução tradicional, um teste por vez

### Paralelo (xdist)
- **Comando:** `pytest -n auto src/test_app.py`
- **Descrição:** Distribui testes entre múltiplos workers

### TIA (Test Impact Analysis)
- **Comando:** `pytest --testmon src/test_app.py`
- **Descrição:** Executa apenas testes impactados por mudanças

## 📈 Hipóteses

- **H1:** TIA reduz significativamente o consumo de energia vs Baseline
- **H2:** Paralelização tem EDP superior (trade-off desfavorável)
- **H3:** Priorização energy-aware melhora APFDe (fase futura)

## 🔧 Troubleshooting

**Erro: "No module named 'src'"**
```bash
# Certifique-se que src/__init__.py existe
touch src/__init__.py

# Teste localmente
python -m pytest src/test_app.py -v
```

**Erro: Eco-CI não coleta métricas**
- Verifique que o runner é self-hosted (não funciona em runners do GitHub)
- Confirme que o runner tem acesso a `/proc/stat`

**CPU Throttling durante testes**
```bash
# Verificar governor
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Definir para performance
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

## 📚 Referências

- Eco-CI: https://github.com/green-coding-berlin/eco-ci-energy-estimation
- pytest-testmon: https://testmon.org/
- pytest-xdist: https://pytest-xdist.readthedocs.io/
