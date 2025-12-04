#!/bin/bash
# Script para baixar todos os artifacts do experimento

echo "📥 Baixando Artifacts do GitHub Actions..."
echo ""

# Criar diretório para dados
mkdir -p data/raw

# Pegar os IDs das últimas 9 execuções bem-sucedidas (ignorando a que falhou - X)
echo "🔍 Identificando execuções bem-sucedidas..."
run_ids=$(gh run list --limit 10 --json databaseId,conclusion --jq '.[] | select(.conclusion=="success") | .databaseId' | head -n 9)

count=0
total=$(echo "$run_ids" | wc -l)

echo "✅ Encontradas $total execuções bem-sucedidas"
echo ""

for run_id in $run_ids; do
    count=$((count + 1))
    echo "[$count/$total] 📦 Baixando run $run_id..."
    
    # Baixar artifacts para pasta específica
    gh run download "$run_id" --dir "data/raw/run-$run_id" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "     ✅ Download completo"
    else
        echo "     ⚠️  Nenhum artifact encontrado (normal para algumas execuções)"
    fi
    echo ""
done

echo "============================================================"
echo "✅ Download Concluído!"
echo "============================================================"
echo ""
echo "📊 Estrutura criada:"
ls -la data/raw/
echo ""
echo "📍 Próximo passo:"
echo "   python3 scripts/metrics.py"
echo ""
