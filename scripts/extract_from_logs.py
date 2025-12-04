#!/usr/bin/env python3
"""
Extrai métricas do Eco-CI diretamente dos logs do GitHub Actions
quando não há artifacts disponíveis.
"""

import subprocess
import json
import re
import os

# IDs das execuções bem-sucedidas
RUN_IDS = [
    19913403957,
    19913397218,
    19913389790,
    19913381708,
    19913374741
]

def get_run_log(run_id):
    """Baixa o log de uma execução"""
    print(f"📥 Baixando log da execução {run_id}...")
    try:
        result = subprocess.run(
            ["gh", "run", "view", str(run_id), "--log"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao baixar log: {e}")
        return None

def extract_metrics_from_log(log_text, run_id):
    """Extrai métricas do Eco-CI do log"""
    
    # Procurar por outputs do Eco-CI (podem estar em formato JSON ou texto)
    # Padrão comum: Energy: XXX mJ, Duration: XXX ms
    
    metrics = {
        'run_id': run_id,
        'energia_mj': None,
        'duracao_ms': None,
        'co2_g': None,
    }
    
    # Tentar encontrar padrões de energia
    energy_match = re.search(r'Energy[:\s]+(\d+\.?\d*)\s*(mJ|J)', log_text, re.IGNORECASE)
    if energy_match:
        value = float(energy_match.group(1))
        unit = energy_match.group(2)
        metrics['energia_mj'] = value if unit == 'mJ' else value * 1000
    
    # Tentar encontrar duração
    duration_match = re.search(r'Duration[:\s]+(\d+\.?\d*)\s*(ms|s)', log_text, re.IGNORECASE)
    if duration_match:
        value = float(duration_match.group(1))
        unit = duration_match.group(2)
        metrics['duracao_ms'] = value if unit == 'ms' else value * 1000
    
    # Tentar encontrar CO2
    co2_match = re.search(r'CO2[:\s]+(\d+\.?\d*)\s*(g|mg)', log_text, re.IGNORECASE)
    if co2_match:
        value = float(co2_match.group(1))
        unit = co2_match.group(2)
        metrics['co2_g'] = value if unit == 'g' else value / 1000
    
    return metrics

def identify_strategy(log_text):
    """Identifica a estratégia pelo nome do workflow"""
    if 'baseline' in log_text.lower():
        return 'baseline'
    elif 'parallel' in log_text.lower():
        return 'parallel'
    elif 'tia' in log_text.lower():
        return 'tia'
    return 'unknown'

def main():
    print("🔍 Extraindo Métricas dos Logs do GitHub Actions...")
    print("")
    
    os.makedirs('data/raw', exist_ok=True)
    results = []
    
    for i, run_id in enumerate(RUN_IDS, 1):
        print(f"\n[{i}/{len(RUN_IDS)}] Processando run {run_id}...")
        
        log = get_run_log(run_id)
        if not log:
            continue
        
        metrics = extract_metrics_from_log(log, run_id)
        strategy = identify_strategy(log)
        
        metrics['estrategia'] = strategy
        
        if metrics['energia_mj']:
            print(f"   ✅ Energia: {metrics['energia_mj']:.2f} mJ")
            print(f"   ✅ Duração: {metrics['duracao_ms']:.2f} ms")
            print(f"   ✅ Estratégia: {strategy}")
            results.append(metrics)
        else:
            print(f"   ⚠️  Não foi possível extrair métricas")
    
    # Salvar em JSON
    if results:
        output_file = 'data/raw/metrics_from_logs.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✅ {len(results)} métricas extraídas")
        print(f"📁 Salvo em: {output_file}")
        print("\n⚠️  NOTA: Métricas extraídas de logs podem estar incompletas.")
        print("   Para dados mais precisos, rode o experimento novamente com os workflows atualizados.")
    else:
        print("\n❌ Nenhuma métrica encontrada nos logs")
        print("\n💡 O Eco-CI pode não ter rodado ou os logs não contêm as métricas.")
        print("   Você precisa:")
        print("   1. Atualizar os workflows para incluir upload de artifacts")
        print("   2. Rodar o experimento novamente")

if __name__ == "__main__":
    main()
