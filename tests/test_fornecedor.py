import pytest
from app.models.fornecedor import Fornecedor

@pytest.fixture
def fornecedor_laboratorio1():
    """
    Fixture para criar um fornecedor de teste.
    """
    return Fornecedor(
        nome="Laboratorio1", 
        cnpj="12345678000199", 
        contato="99999999999"
        )

@pytest.fixture
def fornecedor_laboratorio2():
    """
    Fixture para criar um fornecedor de teste.
    """
    return Fornecedor(
        nome="Laboratorio2", 
        cnpj="98765432000199", 
        contato="88888888888"
        )

@pytest.mark.skip(reason="Testes ignorados por padrão conforme exigência da entrega.")
def test_criacao_fornecedor():
    """
    Testa a criação de um fornecedor.
    """
    fornecedor = Fornecedor(
        nome="Laboratorio1", 
        cnpj="12345678000199", 
        contato="99999999999"
        )
    assert fornecedor.nome == "Laboratorio1"
    assert fornecedor.cnpj == "12345678000199"
    assert fornecedor.contato == "99999999999"
    
@pytest.mark.skip(reason="Testes ignorados por padrão conforme exigência da entrega.")
def test_str_fornecedor(fornecedor_laboratorio1):
    """
    Testa a representação em string de um fornecedor.
    """
    assert str(fornecedor_laboratorio1) == (
        "Fornecedor(nome=Laboratorio1,"
        "cnpj=12345678000199,"
        "contato=99999999999)"
    )
    
@pytest.mark.skip(reason="Testes ignorados por padrão conforme exigência da entrega.")
def test_atributos_fornecedor(fornecedor_laboratorio2):
    """
    Testa os atributos de um fornecedor.
    """
    assert fornecedor_laboratorio2.nome == "Laboratorio2"
    assert fornecedor_laboratorio2.cnpj == "98765432000199"
    assert fornecedor_laboratorio2.contato == "88888888888"
    
@pytest.mark.skip(reason="Testes ignorados por padrão conforme exigência da entrega.")
def test_atributos_fornecedor_incorretos(fornecedor_laboratorio1):
    """
    Testa os atributos de um fornecedor.
    """
    assert fornecedor_laboratorio1.nome != "Laboratorio2"
    assert fornecedor_laboratorio1.cnpj != "98765432000199"
    assert fornecedor_laboratorio1.contato != "88888888888"
