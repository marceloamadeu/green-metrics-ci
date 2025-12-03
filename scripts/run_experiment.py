import os
import time

# ========================================
# CONFIGURAÇÃO PARA TESTE RÁPIDO (10 MIN)
# ========================================
REPETICOES = 3  # Reduzido de 10 para 3
COOLDOWN = 20   # Reduzido de 60s para 20s

WORKFLOWS = [
    "baseline.yml",
    "parallel.yml",
    "tia.yml"
]

print("="*60)
print("🧪 TESTE RÁPIDO - Engenharia de Software Verde")
print("="*60)
print(f"⚙️  {REPETICOES} repetições × {len(WORKFLOWS)} workflows = {REPETICOES * len(WORKFLOWS)} execuções")
print(f"⏱️  Tempo estimado: ~10 minutos")
print("="*60)

for i in range(1, REPETICOES + 1):
    print(f"\n{'='*60}")
    print(f"🔄 RODADA {i} de {REPETICOES}")
    print(f"{'='*60}")
    
    for wf in WORKFLOWS:
        print(f"   ▶️  Disparando: {wf}")
        os.system(f"gh workflow run {wf}")
        
        print(f"   ⏳ Aguardando {COOLDOWN}s...")
        time.sleep(COOLDOWN)

print("\n" + "="*60)
print("✅ Experimento Concluído!")
print("="*60)
print("📍 Verifique a aba Actions no GitHub")
print("📊 Aguarde as execuções finalizarem e baixe os artifacts")