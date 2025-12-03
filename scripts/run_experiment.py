import os
import time

# Configuração
REPETICOES = 10
WORKFLOWS = [
    "baseline.yml",
    "parallel.yml",
    "tia.yml"
]

print("🚀 Iniciando Experimento de Engenharia de Software Verde...")

for i in range(1, REPETICOES + 1):
    print(f"\n--- RODADA {i} de {REPETICOES} ---")
    
    for wf in WORKFLOWS:
        print(f"   ▶️ Disparando: {wf}")
        # Chama o GitHub CLI para iniciar o workflow
        os.system(f"gh workflow run {wf}")
        
        # Espera o tempo do teste + tempo de resfriamento da CPU (Cooldown)
        # Ajuste este tempo conforme a duração real dos seus testes
        print("   ⏳ Aguardando execução e resfriamento (60s)...")
        time.sleep(60) 

print("\n✅ Experimento Concluído! Verifique a aba Actions no GitHub.")
