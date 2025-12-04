#!/bin/bash
# Download automático de todos os artifacts dos workflows simple

echo "📥 Baixando Artifacts dos Workflows Simple..."
echo ""

mkdir -p data/raw

# Função para baixar artifacts de um workflow
download_workflow() {
    local workflow_name=$1
    local estrategia=$2
    
    echo "🔍 Processando workflow: $workflow_name"
    
    # Pegar últimas 10 execuções bem-sucedidas (era 3!)
    run_ids=$(gh run list --workflow="$workflow_name" --limit 15 --json databaseId,conclusion --jq '.[] | select(.conclusion=="success") | .databaseId' | head -n 10)
    
    count=0
    for run_id in $run_ids; do
        count=$((count + 1))
        echo "   [$count/10] 📦 Baixando run $run_id..."
        
        # Baixar para pasta específica
        gh run download "$run_id" --dir "data/raw/${estrategia}-${run_id}" 2>/dev/null
        
        if [ $? -eq 0 ]; then
            # Verificar se baixou o metrics.txt
            if [ -f "data/raw/${estrategia}-${run_id}/metrics-${estrategia}-${run_id}/metrics.txt" ]; then
                echo "        ✅ metrics.txt encontrado"
                # Mover para facilitar análise
                mv "data/raw/${estrategia}-${run_id}/metrics-${estrategia}-${run_id}/metrics.txt" "data/raw/${estrategia}-${run_id}/"
                rm -rf "data/raw/${estrategia}-${run_id}/metrics-${estrategia}-${run_id}"
            elif [ -f "data/raw/${estrategia}-${run_id}/metrics.txt" ]; then
                echo "        ✅ metrics.txt encontrado"
            else
                echo "        ⚠️  metrics.txt não encontrado"
            fi
        else
            echo "        ⚠️  Erro no download ou sem artifacts"
        fi
    done
    echo ""
}

# Baixar de cada workflow
download_workflow "baseline_simple.yml" "baseline"
download_workflow "parallel_simple.yml" "parallel"
download_workflow "tia_simple.yml" "tia"

echo "============================================================"
echo "✅ Download Concluído!"
echo "============================================================"
echo ""
echo "📊 Estrutura criada:"
ls -d data/raw/*/ 2>/dev/null | head -10
echo ""
echo "📍 Verificar quantos arquivos foram baixados:"
find data/raw -name "metrics.txt" | wc -l
echo ""
echo "📍 Próximo passo:"
echo "   python3 scripts/analyze_simple_metrics.py"
echo ""