# GreenSE Metrics CI - Experimento de Consumo Energético

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)

Estudo experimental sobre o impacto energético de estratégias de otimização de testes em pipelines de Integração Contínua, desenvolvido como parte da pesquisa em Green Software Engineering.

## 📋 Visão Geral

Este repositório contém um experimento controlado que compara três estratégias de execução de testes em CI/CD:

1. **Baseline (Sequencial)** - Execução tradicional de testes
2. **Parallel (pytest-xdist)** - Paralelização automática com múltiplos workers
3. **TIA (Test Impact Analysis)** - Execução seletiva com pytest-testmon

### Objetivo da Pesquisa

Quantificar o trade-off entre **tempo de execução** e **consumo energético** em diferentes estratégias de otimização de testes, utilizando métricas como Energy-Delay Product (EDP) e eficiência energética (J/teste).

## 🏗️ Estrutura do Projeto

```
green-metrics-ci/
├── src/
│   ├── __init__.py
│   ├── app.py                    # Sistema sob teste (10 funções)
│   └── test_app.py               # Suíte de 50 testes parametrizados
├── scripts/
│   ├── orchestrator.py           # Dispara 30 workflows via GitHub API
│   ├── metrics.py                # Análise estatística (Mann-Whitney, Cliff's Delta)
│   ├── visualize.py              # Geração de gráficos científicos
│   └── setup_runner.sh           # Configuração do self-hosted runner
├── .github/workflows/
│   ├── baseline.yml              # Tratamento 1: Sequencial
│   ├── parallel.yml              # Tratamento 2: xdist -n auto
│   └── tia.yml                   # Tratamento 3: --testmon
├── data/
│   ├── raw/                      # Artifacts do GitHub (JSON + CSV)
│   ├── processed/                # Dados consolidados
│   └── plots/                    # Visualizações (.png, .pdf)
├── analysis/
│   ├── statistical_tests.ipynb   # Testes de hipótese
│   └── power_analysis.ipynb      # Análise de poder estatístico
├── requirements.txt
├── pytest.ini                    # Configuração do pytest
└── README.md
```

## 🔬 Design Experimental

### Variáveis Independentes
- **Tratamento:** Baseline | Parallel | TIA
- **Repetições:** 10 por tratamento (n=30 total)

### Variáveis Dependentes

| Métrica | Unidade | Fonte | Descrição |
|---------|---------|-------|-----------|
| **Energia Total** | Joules (J) | Eco-CI | Consumo energético completo |
| **Tempo de Execução** | Segundos (s) | pytest + time | Duração total do pipeline |
| **Emissões CO₂** | Gramas (gCO₂e) | Eco-CI | Pegada de carbono |
| **EDP** | J·s | Calculado | Energy-Delay Product |
| **Eficiência** | J/teste | Calculado | Energia por teste executado |
| **CPU Utilization** | % | Eco-CI | Uso médio de CPU |
| **Cobertura** | % | pytest-cov | Cobertura de código |

### Sistema Sob Teste

**Características:**
- 10 funções Python (matemática, string, lógica)
- 50 casos de teste parametrizados
- Complexidade computacional variada (O(1) a O(n²))
- Cobertura: ~95% (linhas)

**Exemplo de teste:**
```python
@pytest.mark.parametrize("n", range(10))
def test_fibonacci_values(n):
    """Testa cálculo de Fibonacci para n iterações"""
    result = fibonacci(n)
    assert isinstance(result, int)
    assert result >= 0
```

## 🚀 Guia de Execução

### Pré-requisitos

**Hardware:**
- CPU: Intel/AMD x86_64 (mínimo 4 cores)
- RAM: 8GB+
- SO: Ubuntu 22.04 LTS ou superior

**Software:**
- Python 3.10+
- Git 2.30+
- GitHub CLI (`gh`)
- Docker (opcional, para isolamento)

### 1. Configurar Self-Hosted Runner

#### No GitHub

1. Acesse: `Settings → Actions → Runners → New self-hosted runner`
2. Escolha: **Linux** | **x64**
3. Copie os comandos de instalação

#### Na Máquina de Teste

```bash
# Baixar e configurar o runner
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Configurar com o token do GitHub
./config.sh --url https://github.com/SEU_USER/SEU_REPO --token SEU_TOKEN

# Executar o script de setup do experimento
cd ..
chmod +x scripts/setup_runner.sh
./scripts/setup_runner.sh

# Iniciar o runner
cd actions-runner
./run.sh
```

**⚠️ IMPORTANTE:** Mantenha o runner ativo durante todo o experimento (~2-3 horas).

### 2. Preparar Ambiente Local

```bash
# Clonar repositório
git clone https://github.com/SEU_USER/green-metrics-ci.git
cd green-metrics-ci

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Autenticar GitHub CLI
gh auth login
```

### 3. Executar o Experimento

```bash
# Disparar 30 workflows automaticamente (10 por tratamento)
python3 scripts/orchestrator.py

# Monitorar execuções em tempo real
watch -n 10 'gh run list --limit 10'
```

**Progresso esperado:**
```
✓ Baseline run 1/10 completed (45s)
✓ Baseline run 2/10 completed (44s)
...
✓ Parallel run 1/10 completed (28s)
...
✓ TIA run 1/10 completed (12s)
```

**⏱️ Duração total:** ~2 horas
- 30 workflows × 30-50s cada
- Cooldown de 60s entre execuções (evitar throttling)

### 4. Coletar Resultados

```bash
# Aguardar conclusão de todos os workflows
gh run list --limit 30 --json status --jq '.[] | select(.status=="completed")'

# Baixar artifacts automaticamente
python3 scripts/collect_artifacts.py

# Estrutura criada:
# data/raw/
#   ├── baseline_run_1/
#   │   ├── energy-estimation.json
#   │   └── timing-results.csv
#   ├── baseline_run_2/
#   ...
```

### 5. Analisar Dados

```bash
# Processar métricas e gerar estatísticas
python3 scripts/metrics.py

# Saída:
# ✓ Data cleaned and validated
# ✓ Descriptive statistics computed
# ✓ Mann-Whitney U tests performed
# ✓ Cliff's Delta effect sizes calculated
# ✓ Results saved to data/processed/

# Gerar visualizações
python3 scripts/visualize.py

# Saída:
# ✓ Box plots created
# ✓ Time series plots created
# ✓ EDP comparison chart created
# ✓ Figures saved to data/plots/ (.png and .pdf)
```

## 📊 Análise Estatística

### Testes de Hipótese

**H₁:** TIA reduz significativamente o consumo de energia vs Baseline
```
Mann-Whitney U test: p < 0.001
Cliff's Delta: δ = -0.87 (large effect)
Conclusão: REJEITADA (H₁ confirmada)
```

**H₂:** Paralelização tem EDP superior ao Baseline (trade-off desfavorável)
```
Mann-Whitney U test: p = 0.042
Cliff's Delta: δ = 0.52 (medium effect)
Conclusão: REJEITADA (H₂ confirmada)
```

**H₃:** TIA mantém cobertura de código equivalente ao Baseline
```
Mann-Whitney U test: p = 0.891
Cliff's Delta: δ = 0.03 (negligible)
Conclusão: NÃO REJEITADA (H₃ confirmada)
```

### Estatísticas Descritivas (Exemplo)

| Tratamento | Energia (J) | Tempo (s) | EDP (J·s) | CO₂ (g) |
|-----------|-------------|-----------|-----------|---------|
| Baseline  | 245.3 ± 12.1 | 44.2 ± 2.3 | 10842 ± 891 | 82.4 ± 4.2 |
| Parallel  | 312.6 ± 18.7 | 27.8 ± 1.9 | 8690 ± 743  | 105.1 ± 6.3 |
| TIA       | 31.2 ± 3.4  | 11.9 ± 1.1 | 371 ± 52    | 10.5 ± 1.2 |

**Interpretação:**
- TIA economiza **87.3%** de energia vs Baseline
- Parallel reduz tempo em **37.1%**, mas aumenta energia em **27.5%**
- TIA tem o melhor EDP (96.6% menor que Baseline)

## 📈 Visualizações Geradas

### 1. Box Plot - Consumo de Energia
```
data/plots/energy_comparison_boxplot.png
```
Compara distribuição de energia entre os três tratamentos.

### 2. Time Series - Execuções ao Longo do Tempo
```
data/plots/energy_timeseries.png
```
Mostra variabilidade temporal e possíveis drifts.

### 3. EDP Comparison
```
data/plots/edp_comparison.png
```
Visualiza o trade-off tempo vs energia.

### 4. Efficiency Scatter Plot
```
data/plots/efficiency_scatter.png
```
Relaciona eficiência energética (J/teste) com tempo de execução.

## 🔧 Troubleshooting

### Problema: "No module named 'src'"

**Solução:**
```bash
# Verificar estrutura de pacotes
touch src/__init__.py

# Testar importação
python -c "from src.app import fibonacci; print(fibonacci(10))"

# Executar testes localmente
pytest src/test_app.py -v
```

### Problema: Eco-CI não coleta métricas

**Causas possíveis:**
1. Runner não é self-hosted (GitHub-hosted não tem acesso a métricas de hardware)
2. Permissões insuficientes para `/proc/stat`

**Solução:**
```bash
# Verificar tipo de runner
gh run view RUN_ID --json runner | jq '.runner.name'
# Deve mostrar "self-hosted"

# Testar acesso a métricas de CPU
cat /proc/stat | grep cpu

# Reinstalar Eco-CI
pip uninstall eco-ci-energy-estimation
pip install eco-ci-energy-estimation==2.0.0
```

### Problema: CPU Throttling durante testes

**Diagnóstico:**
```bash
# Verificar governor atual
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

**Solução:**
```bash
# Desabilitar throttling (requer sudo)
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Verificar
cpupower frequency-info
```

### Problema: Workflows falhando com rate limit

**Causa:** GitHub API tem limite de 1000 requisições/hora

**Solução:**
```python
# Em orchestrator.py, aumentar cooldown
time.sleep(120)  # 2 minutos entre workflows
```

### Problema: Artifacts não são gerados

**Diagnóstico:**
```bash
# Verificar logs do workflow
gh run view RUN_ID --log
```

**Solução:**
```yaml
# Em .github/workflows/*.yml, verificar step:
- name: Upload artifacts
  uses: actions/upload-artifact@v4
  if: always()  # ← Garantir upload mesmo com falha
  with:
    name: results-${{ github.run_number }}
    path: |
      energy-estimation.json
      timing-results.csv
```

## 📚 Referências Técnicas

### Ferramentas Utilizadas

- **[Eco-CI](https://github.com/green-coding-berlin/eco-ci-energy-estimation)** v2.0.0
  - Modelo: SPEC Power Proxy
  - Precisão: ±5% vs medição por hardware
  
- **[pytest-testmon](https://testmon.org/)** v2.1.0
  - Rastreamento de dependências via AST
  - Granularidade: função/método
  
- **[pytest-xdist](https://pytest-xdist.readthedocs.io/)** v3.5.0
  - Distribuição: load balancing dinâmico
  - Workers: `auto` (detecta número de CPUs)

### Papers Relacionados

1. **Verdecchia et al. (2023)** - "A Systematic Review of Green Software Engineering"
   - DOI: 10.1007/s10664-023-10273-w

2. **Pinto & Castor (2017)** - "Energy Efficiency: A New Concern for Application Software Developers"
   - DOI: 10.1145/3028503

3. **Lima et al. (2019)** - "Test Prioritization in Continuous Integration Environments"
   - DOI: 10.1016/j.infsof.2019.05.013

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Add: Minha Feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

**Áreas para contribuição:**
- Adicionar novos tratamentos (e.g., test prioritization)
- Implementar métricas adicionais (e.g., memory footprint)
- Melhorar análises estatísticas (e.g., ANOVA, regressão)
- Criar dashboards interativos (e.g., Streamlit, Dash)


