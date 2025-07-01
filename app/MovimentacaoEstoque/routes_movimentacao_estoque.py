from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.settings import get_db
from app.MovimentacaoEstoque.schema_movimentacao_estoque import MovimentacaoEstoqueCreate, MovimentacaoEstoqueRead
from app.MovimentacaoEstoque import service_movimentacao_estoque
from app.security import get_current_user
from app.Funcionario.model_funcionario import Funcionario

router = APIRouter(prefix="/movimentacao-estoque", tags=["Movimentação Estoque"])

@router.post("/", response_model=MovimentacaoEstoqueRead)
def create_movimentacao(movimentacao: MovimentacaoEstoqueCreate, db: Session = Depends(get_db), usuario: Funcionario = Depends(get_current_user)):
    # Forçar o responsável para o usuário autenticado
    movimentacao_dict = movimentacao.dict()
    movimentacao_dict["responsavel_id"] = usuario.id
    from app.MovimentacaoEstoque.schema_movimentacao_estoque import MovimentacaoEstoqueCreate as MovCreate
    nova_movimentacao = MovCreate(**movimentacao_dict)
    return service_movimentacao_estoque.create_movimentacaoestoque(db, nova_movimentacao)

@router.get("/", response_model=List[MovimentacaoEstoqueRead])
def get_all_movimentacoes(db: Session = Depends(get_db)):
    return service_movimentacao_estoque.get_all_movimentacoes(db)

@router.get("/{id}", response_model=MovimentacaoEstoqueRead)
def get_movimentacao_by_id(id: int, db: Session = Depends(get_db)):
    movimentacao = service_movimentacao_estoque.get_movimentacao_by_id(db, id)
    if not movimentacao:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    return movimentacao

@router.put("/{id}", response_model=MovimentacaoEstoqueRead)
def update_movimentacao(id: int, movimentacao: MovimentacaoEstoqueCreate, db: Session = Depends(get_db)):
    return service_movimentacao_estoque.update_movimentacao(db, id, movimentacao)

@router.delete("/{id}")
def delete_movimentacao(id: int, db: Session = Depends(get_db)):
    return service_movimentacao_estoque.delete_movimentacao(db, id)
