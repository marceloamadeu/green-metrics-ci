import os
import time

estrategias = ["baseline", "parallel"]

for est in estrategias:
    print(f"--- Iniciando bateria para: {est} ---")
    for i in range(1, 11): # 10 Repetições
        print(f"Execução {i}/10...")
        # Dispara o workflow (requer GitHub CLI instalado: gh)
        os.system(f'gh workflow run experiment.yml -f strategy={est}')
        
        # Espera 2 minutos (tempo do teste + cooldown)
        time.sleep(120)
