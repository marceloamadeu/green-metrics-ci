# 1. Organizar arquivos
touch src/__init__.py
chmod +x scripts/setup_runner.sh

# 2. Preparar ambiente
./scripts/setup_runner.sh

# 3. Executar experimento
python3 scripts/orchestrator.py

# 4. Após 2 horas, coletar dados
mkdir -p data/raw
gh run list --limit 30
# Baixar cada artifact manualmente ou em loop

# 5. Analisar
python3 scripts/metrics.py