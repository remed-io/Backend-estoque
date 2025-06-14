# app/api/medicamento_endpoint.py

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.settings import SessionLocal
from app.schemas.medicamento_schema import (
    MedicamentoCreate,
    MedicamentoRead
)
from app.services import medicamento_service

router = APIRouter(prefix="/medicamentos", tags=["Medicamentos"])

# Reusing the get_db dependency as it's a common pattern
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/",
    response_model=MedicamentoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo medicamento",
    response_description="O medicamento criado com sucesso"
)
def create_medicamento(medicamento: MedicamentoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo registro de medicamento no banco de dados.

    - **nome**: Nome do medicamento (obrigatório)
    - **descricao**: Descrição detalhada do medicamento (opcional)
    - **principio_ativo**: Princípio ativo do medicamento (opcional)
    - **tarja**: Cor da tarja do medicamento (opcional)
    - **restricoes**: Restrições de uso do medicamento (opcional)
    - **fabricante**: Fabricante do medicamento (opcional)
    - **registro_anvisa**: Número de registro na ANVISA (opcional)
    """
    return medicamento_service.create_medicamento(db, medicamento)

@router.get(
    "/",
    response_model=List[MedicamentoRead],
    summary="Lista todos os medicamentos",
    response_description="Uma lista de medicamentos"
)
def get_all_medicamentos(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de itens para pular"),
    limit: int = Query(100, ge=1, le=200, description="Número máximo de itens para retornar"),
):
    """
    Retorna uma lista de todos os medicamentos cadastrados no sistema.

    - **skip**: Quantidade de registros para pular (útil para paginação).
    - **limit**: Quantidade máxima de registros para retornar.
    """
    return medicamento_service.get_all_medicamentos(db, skip=skip, limit=limit)

@router.get(
    "/{id}",
    response_model=MedicamentoRead,
    summary="Obtém um medicamento por ID",
    response_description="Os detalhes do medicamento solicitado"
)
def get_medicamento_by_id(id: int, db: Session = Depends(get_db)):
    """
    Retorna um medicamento específico com base no seu ID.

    - **id**: O ID do medicamento a ser retornado.
    """
    medicamento = medicamento_service.get_medicamento_by_id(db, id)
    if not medicamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medicamento não encontrado")
    return medicamento

@router.get(
    "/search/", # Use a specific path for search to avoid conflicts with /{id}
    response_model=List[MedicamentoRead],
    summary="Busca medicamentos por termo",
    response_description="Uma lista de medicamentos que correspondem à busca"
)
def search_medicamentos(
    query: str = Query(..., min_length=2, description="Termo de busca (nome, princípio ativo ou fabricante)"),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de itens para pular"),
    limit: int = Query(100, ge=1, le=200, description="Número máximo de itens para retornar"),
):
    """
    Realiza uma busca por medicamentos com base em um termo de consulta que pode corresponder ao nome, princípio ativo ou fabricante.

    - **query**: O termo de busca.
    - **skip**: Quantidade de registros para pular.
    - **limit**: Quantidade máxima de registros para retornar.
    """
    return medicamento_service.search_medicamentos(db, query=query, skip=skip, limit=limit)

@router.put(
    "/{id}",
    response_model=MedicamentoRead,
    summary="Atualiza um medicamento existente",
    response_description="O medicamento atualizado"
)
def update_medicamento(id: int, medicamento: MedicamentoCreate, db: Session = Depends(get_db)):
    """
    Atualiza as informações de um medicamento existente.

    - **id**: O ID do medicamento a ser atualizado.
    - **medicamento**: Os novos dados do medicamento.
    """
    return medicamento_service.update_medicamento(db, id, medicamento)

@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Deleta um medicamento",
    response_description="Mensagem de sucesso da remoção"
)
def delete_medicamento(id: int, db: Session = Depends(get_db)):
    """
    Remove um medicamento do banco de dados.

    - **id**: O ID do medicamento a ser removido.
    """
    return medicamento_service.delete_medicamento(db, id)