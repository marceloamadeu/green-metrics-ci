import pytest
from src.app import cpu_intensive_task, memory_intensive_task, io_simulation

# Testes de CPU (Carga Alta)
@pytest.mark.parametrize("n", )
def test_cpu_factorial(n):
    result = cpu_intensive_task(n)
    assert result > 0

# Teste de Erro
def test_cpu_error():
    with pytest.raises(ValueError):
        cpu_intensive_task(-1)

# Testes de Memória
@pytest.mark.parametrize("size", )
def test_memory_sort(size):
    sorted_list = memory_intensive_task(size)
    assert len(sorted_list) == size
    assert sorted_list <= sorted_list[-1]

# Teste de I/O
def test_io_wait():
    res = io_simulation(0.1)
    assert res == "Done"