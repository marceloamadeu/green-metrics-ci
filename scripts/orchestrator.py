import subprocess
import time
import sys
import os

# Configurações
# Substitua pelo seu usuário/repo se necessário, ou o GH CLI infere
WORKFLOWS = [
    "baseline.yml",
    "parallel.yml",
    "tia.yml"
]
REPETITIONS = 10 # 10 repetições como pedido pelo professor

def run_workflow(workflow_file):
    print(f"🚀 Disparando workflow: {workflow_file}...")
    
    # CORREÇÃO: Comando definido como lista de strings
    cmd = ["gh", "workflow", "run", workflow_file]
    
    try:
        # check=True lança erro se o comando falhar
        subprocess.run(cmd, check=True)
        print(f"✅ {workflow_file} iniciado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar {workflow_file}: {e}")
    except FileNotFoundError:
        print("❌ Erro: 'gh' CLI não encontrado. Instale o GitHub CLI.")
        sys.exit(1)

def main():
    print(f"=== Iniciando Experimento Green Metrics: {REPETITIONS} repetições ===")
    
    for i in range(1, REPETITIONS + 1):
        print(f"\n--- RODADA {i}/{REPETITIONS} ---")
        
        for wf in WORKFLOWS:
            run_workflow(wf)
            
            # Intervalo de resfriamento (Cooldown)
            # Importante para Green Software para evitar thermal throttling na CPU
            print("⏳ Aguardando 60s para resfriamento e conclusão...")
            time.sleep(60)

    print("\n=== Experimento Finalizado ===")
    print("Vá para a aba 'Actions' no GitHub para ver os resultados de energia.")

if __name__ == "__main__":
    main()