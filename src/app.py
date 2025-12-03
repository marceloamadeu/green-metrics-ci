import math
import random
import time

def cpu_intensive_task(n):
    """
    Calcula o fatorial de n. 
    Gera carga de CPU pura para o teste.
    """
    if n < 0:
        raise ValueError("Número deve ser não-negativo")
    
    # Loop para garantir consumo de CPU
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def memory_intensive_task(size):
    """
    Cria e ordena uma lista grande.
    Gera carga de Memória e CPU.
    """
    # Gera lista de números aleatórios
    data = [random.random() for _ in range(size)]
    # Ordena a lista (Timsort é O(n log n))
    return sorted(data)

def io_simulation(duration):
    """
    Simula uma espera de I/O (ex: banco de dados).
    """
    time.sleep(duration)
    return "Done"

if __name__ == "__main__":
    print("Executando teste manual...")
    print(f"Fatorial(100): {str(cpu_intensive_task(100))[:10]}...")