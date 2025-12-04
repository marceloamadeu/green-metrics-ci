import subprocess
import time
import sys
import os

# ========================================
# CONFIGURAÇÃO PARA TESTE RÁPIDO (10 MIN)
# ========================================
WORKFLOWS = [
    "baseline_simple.yml",
    "parallel_simple.yml",
    "tia_simple.yml"
]
REPETITIONS = 3  # Reduzido de 10 para 3 (teste rápido)
COOLDOWN = 20    # Reduzido de 60s para 20s

# ========================================
# Para o experimento real, use:
# REPETITIONS = 10
# COOLDOWN = 60
# ========================================

def run_workflow(workflow_file):
    """Dispara um workflow no GitHub Actions via CLI"""
    print(f"🚀 Disparando workflow: {workflow_file}...")
    
    cmd = ["gh", "workflow", "run", workflow_file]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ {workflow_file} iniciado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar {workflow_file}: {e}")
    except FileNotFoundError:
        print("❌ Erro: 'gh' CLI não encontrado. Instale o GitHub CLI.")
        print("   https://cli.github.com/")
        sys.exit(1)

def main():
    print("="*60)
    print("🧪 TESTE RÁPIDO - Green Metrics CI")
    print("="*60)
    print(f"⚙️  Configuração:")
    print(f"   • Repetições: {REPETITIONS}")
    print(f"   • Workflows: {len(WORKFLOWS)}")
    print(f"   • Cooldown: {COOLDOWN}s")
    print(f"   • Total de execuções: {REPETITIONS * len(WORKFLOWS)}")
    print(f"   • Tempo estimado: ~{int((REPETITIONS * len(WORKFLOWS) * 30 + REPETITIONS * len(WORKFLOWS) * COOLDOWN) / 60)} minutos")
    print("="*60)
    
    input("\n⏸️  Pressione ENTER para iniciar o experimento...")
    
    start_time = time.time()
    
    for i in range(1, REPETITIONS + 1):
        print(f"\n{'='*60}")
        print(f"🔄 RODADA {i}/{REPETITIONS}")
        print(f"{'='*60}")
        
        for wf in WORKFLOWS:
            run_workflow(wf)
            
            # Intervalo de resfriamento (Cooldown)
            print(f"⏳ Aguardando {COOLDOWN}s para resfriamento...")
            time.sleep(COOLDOWN)
        
        elapsed = int(time.time() - start_time)
        remaining_reps = REPETITIONS - i
        estimated_remaining = int((remaining_reps * len(WORKFLOWS) * 30 + remaining_reps * len(WORKFLOWS) * COOLDOWN) / 60)
        
        print(f"\n📊 Progresso: {i}/{REPETITIONS} rodadas completas")
        print(f"⏱️  Tempo decorrido: {elapsed//60}min {elapsed%60}s")
        print(f"⏱️  Tempo restante estimado: ~{estimated_remaining} min")
    
    total_time = int(time.time() - start_time)
    print("\n" + "="*60)
    print("✅ EXPERIMENTO FINALIZADO!")
    print("="*60)
    print(f"⏱️  Tempo total: {total_time//60}min {total_time%60}s")
    print(f"📊 Total de workflows disparados: {REPETITIONS * len(WORKFLOWS)}")
    print("\n📍 Próximos passos:")
    print("   1. Vá para a aba 'Actions' no GitHub para verificar as execuções")
    print("   2. Aguarde todas as execuções concluírem (~5-10 min)")
    print("   3. Baixe os artifacts: gh run list --limit 10")
    print("   4. Analise os dados: python3 scripts/metrics.py")

if __name__ == "__main__":
    main()