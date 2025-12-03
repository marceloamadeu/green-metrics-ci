import pytest
from src.app import cpu_intensive_task, memory_intensive_task, io_simulation

# --- Testes de Unidade (Carga de CPU) ---

@pytest.mark.parametrize("n", )
def test_cpu_factorial(n):
    """Testa cálculo de fatorial com diferentes cargas."""
    result = cpu_intensive_task(n)
    assert result > 0

def test_cpu_error():
    """Testa erro com input negativo."""
    with pytest.raises(ValueError):
        cpu_intensive_task(-1)

# --- Testes de Integração Simulados (Carga de Memória) ---

@pytest.mark.parametrize("size", )
def test_memory_sort(size):
    """Testa ordenação de listas grandes."""
    sorted_list = memory_intensive_task(size)
    assert len(sorted_list) == size
    assert sorted_list <= sorted_list[-1]

# --- Testes de I/O (Espera) ---

def test_io_wait():
    """Simula uma chamada lenta de API ou Banco."""
    res = io_simulation(0.5) # 500ms de espera
    assert res == "Done"