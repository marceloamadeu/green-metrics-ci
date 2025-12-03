import os
import sys
import subprocess
import time

def main():
    print("Initializing Green Metrics Orchestration...")
    
    # Definição de Arquivos de Saída
    results_xml = "test-results.xml"
    
    # CORREÇÃO CRÍTICA: Atribuição completa da variável 'cmd'
    # Utilizando lista para segurança e clareza.
    # --testmon: Ativa a seleção inteligente de testes
    # --junitxml: Gera relatório XML para consumo posterior
    cmd = [
        "pytest", 
        "--testmon", 
        f"--junitxml={results_xml}",
        "-vv"
    ]
    
    start_time = time.time()
    
    try:
        print(f"Executing Command: {' '.join(cmd)}")
        
        # Execução síncrona com captura de output
        # Em uma implementação avançada, usaríamos Popen para monitoramento paralelo
        result = subprocess.run(
            cmd,
            check=True,         # Levanta exceção se o pytest falhar (testes quebrados)
            capture_output=True,
            text=True,
            env=os.environ.copy() # Garante que variáveis de ambiente do CI passem
        )
        
        duration = time.time() - start_time
        print(f"Tests Completed Successfully in {duration:.2f}s")
        print("Output snippet:", result.stdout[:500])
        
        # Gera o resumo Markdown para o GitHub Actions
        generate_summary(duration, "Success")

    except subprocess.CalledProcessError as e:
        duration = time.time() - start_time
        print(f"Test Execution Failed after {duration:.2f}s")
        print("Error Output:", e.stderr)
        
        generate_summary(duration, "Failure")
        sys.exit(1) # Falha o pipeline explicitamente

def generate_summary(duration, status):
    """Escreve o resumo da execução no GITHUB_STEP_SUMMARY"""
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        markdown = f"""
### 🌿 Green Metrics CI Report

| Metric | Value |
| :--- | :--- |
| **Status** | {status} |
| **Execution Time** | {duration:.2f}s |
| **Optimization Strategy** | Test Impact Analysis (TIA) |
        """
        with open(summary_path, "a") as f:
            f.write(markdown)

if __name__ == "__main__":
    main()