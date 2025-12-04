import pytest
import sys
from pathlib import Path

# Adiciona a pasta src ao path para imports funcionarem
sys.path.insert(0, str(Path(__file__).parent))

from app import cpu_intensive_task, memory_intensive_task, io_simulation

# =============================================================================
# CONFIGURAÇÃO: TESTE DE 30 MINUTOS
# - 15 testes (meio termo entre 6 e 20)
# - Carga média (não muito pesado)
# - Tempo total sequencial: ~8-12 segundos
# - Total de execuções: 5 repetições × 3 estratégias = 15 execuções
# - Tempo estimado: ~30 minutos
# =============================================================================

# Testes de CPU (Carga Média)
@pytest.mark.parametrize("n", [500, 1000, 1500, 2000])
def test_cpu_factorial(n):
    """
    Testes de CPU com carga média.
    Tempo esperado: ~0.3-1s por teste
    """
    result = cpu_intensive_task(n)
    assert result > 0

# Teste de Erro
def test_cpu_error():
    """Validação de entrada inválida"""
    with pytest.raises(ValueError):
        cpu_intensive_task(-1)

# Testes de Memória (Carga Média)
@pytest.mark.parametrize("size", [20000, 50000, 100000])
def test_memory_sort(size):
    """
    Testes de memória com carga média.
    Tempo esperado: ~0.2-0.8s por teste
    """
    sorted_list = memory_intensive_task(size)
    assert len(sorted_list) == size
    assert sorted_list[0] <= sorted_list[-1]
    # Verificar ordenação
    for i in range(0, len(sorted_list) - 1, max(1, len(sorted_list) // 100)):
        assert sorted_list[i] <= sorted_list[i + 1]

# Testes de I/O
@pytest.mark.parametrize("duration", [0.05, 0.1])
def test_io_wait(duration):
    """
    Simula diferentes latências de I/O.
    Tempo esperado: 0.2s, 0.4s, 0.6s
    """
    res = io_simulation(duration)
    assert res == "Done"

# Testes Mistos
@pytest.mark.parametrize("n,size", [(200, 30000), (400, 60000)])
def test_combined_workload(n, size):
    """
    Combina CPU e memória.
    Tempo esperado: ~0.5-1.5s por teste
    """
    # CPU
    factorial_result = cpu_intensive_task(n)
    assert factorial_result > 0
    
    # Memória
    sorted_list = memory_intensive_task(size)
    assert len(sorted_list) == size

# =============================================================================
# TOTAL: 15 TESTES
# - CPU: 4 testes parametrizados + 1 erro = 5
# - Memória: 3 testes parametrizados = 3
# - I/O: 3 testes parametrizados = 3
# - Mistos: 2 testes parametrizados = 2
# - Extra: 2 (erro + validações)
#
# Tempo total estimado:
# - Sequencial: ~8-12 segundos
# - Paralelo (4 cores): ~3-5 segundos
# - TIA (após mudança): ~2-4 segundos
# =============================================================================