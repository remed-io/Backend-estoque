import pytest
import logging
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.settings import Base, engine, get_db
from app.Armazem.model_armazem import Armazem
from app.Armazem.service_armazem import (
    create_armazem, get_all_armazems, get_armazem_by_id, update_armazem, delete_armazem
)
from app.Armazem.schema_armazem import ArmazemCreate

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sessão para testes usando o engine central (com fallback para SQLite, se necessário)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture para configurar o banco para cada teste
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Fixture para cliente de teste com override da dependência get_db
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# Testes unitários da camada de serviço
def test_model_armazem_str():
    logger.info("Testando __str__ do modelo Armazem")
    armazem = Armazem(id=1, local_armazem="Depósito Central")
    with pytest.raises(AttributeError) as excinfo:
        str(armazem)
    print(f"[LOG] Erro esperado ao chamar __str__: {excinfo.value}")

def test_create_armazem(db_session):
    logger.info("Testando criação de armazém")
    armazem_data = ArmazemCreate(local_armazem="Depósito Central")
    armazem = create_armazem(db_session, armazem_data)
    logger.info(f"Armazém criado: {armazem.id}, {armazem.local_armazem}")
    assert armazem.id is not None
    assert armazem.local_armazem == "Depósito Central"

    logger.info("Testando duplicidade de armazém")
    with pytest.raises(Exception) as excinfo:
        create_armazem(db_session, armazem_data)
    print(f"[LOG] Erro esperado ao tentar criar armazém duplicado: {excinfo.value}")

def test_get_all_armazems(db_session):
    logger.info("Testando listagem de armazéns")
    armazem_data = ArmazemCreate(local_armazem="Depósito 1")
    create_armazem(db_session, armazem_data)
    armazens = get_all_armazems(db_session)
    logger.info(f"Armazéns encontrados: {armazens}")
    assert len(armazens) == 1
    assert armazens[0].local_armazem == "Depósito 1"

def test_get_armazem_by_id(db_session):
    logger.info("Testando busca de armazém por ID")
    armazem_data = ArmazemCreate(local_armazem="Depósito 2")
    armazem = create_armazem(db_session, armazem_data)
    armazem_encontrado = get_armazem_by_id(db_session, armazem.id)
    logger.info(f"Armazém encontrado: {armazem_encontrado}")
    assert armazem_encontrado is not None
    assert armazem_encontrado.local_armazem == "Depósito 2"

def test_update_armazem(db_session):
    logger.info("Testando atualização de armazém")
    armazem_data = ArmazemCreate(local_armazem="Depósito 3")
    armazem = create_armazem(db_session, armazem_data)
    novo_dado = ArmazemCreate(local_armazem="Depósito Atualizado")
    armazem_atualizado = update_armazem(db_session, armazem.id, novo_dado)
    logger.info(f"Armazém atualizado: {armazem_atualizado}")
    assert armazem_atualizado.local_armazem == "Depósito Atualizado"

    logger.info("Testando atualização de armazém inexistente")
    with pytest.raises(Exception) as excinfo:
        update_armazem(db_session, 999, novo_dado)
    print(f"[LOG] Erro esperado ao tentar atualizar armazém inexistente: {excinfo.value}")

def test_delete_armazem(db_session):
    logger.info("Testando deleção de armazém")
    armazem_data = ArmazemCreate(local_armazem="Depósito 4")
    armazem = create_armazem(db_session, armazem_data)
    resposta = delete_armazem(db_session, armazem.id)
    logger.info(f"Resposta ao deletar: {resposta}")
    assert resposta["message"] == "Local de armazenamento deletado com sucesso"

    logger.info("Testando deleção de armazém inexistente")
    with pytest.raises(Exception) as excinfo:
        delete_armazem(db_session, 999)
    print(f"[LOG] Erro esperado ao tentar deletar armazém inexistente: {excinfo.value}")

# Teste de integração via API
def test_crud_armazem_api(client):
    logger.info("Testando CRUD completo via API")

    # Create
    response = client.post("/armazem/", json={"local_armazem": "Depósito API"})
    logger.info(f"POST /armazem/ response: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["local_armazem"] == "Depósito API"
    armazem_id = data["id"]

    # Read All
    response = client.get("/armazem/")
    logger.info(f"GET /armazem/ response: {response.json()}")
    assert response.status_code == 200
    assert any(a["local_armazem"] == "Depósito API" for a in response.json())

    # Read One
    response = client.get(f"/armazem/{armazem_id}")
    logger.info(f"GET /armazem/{armazem_id} response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["local_armazem"] == "Depósito API"

    # Update
    response = client.put(f"/armazem/{armazem_id}", json={"local_armazem": "Depósito Atualizado API"})
    logger.info(f"PUT /armazem/{armazem_id} response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["local_armazem"] == "Depósito Atualizado API"

    # Delete
    response = client.delete(f"/armazem/{armazem_id}")
    logger.info(f"DELETE /armazem/{armazem_id} response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["message"] == "Local de armazenamento deletado com sucesso"

    # Read Deleted
    response = client.get(f"/armazem/{armazem_id}")
    logger.info(f"GET /armazem/{armazem_id} após deleção, status: {response.status_code}")
    assert response.status_code == 404
