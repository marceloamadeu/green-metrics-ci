import pytest
from app import processamento_pesado

# Gera 50 casos de teste automaticamente
@pytest.mark.parametrize("entrada", range(50))
def test_processamento(entrada):
    assert processamento_pesado(entrada) == entrada * entrada
