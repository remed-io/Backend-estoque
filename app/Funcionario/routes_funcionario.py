from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.settings import get_db
from app.Funcionario.schema_funcionario import (
    FuncionarioCreate,
    FuncionarioRead,
    FuncionarioLogin
)
from app.Funcionario import service_funcionario
from fastapi import Response
import logging

router = APIRouter(prefix="/funcionario", tags=["Funcionário"])

@router.post("/", response_model=FuncionarioRead)
def create_funcionario(funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    return service_funcionario.create_funcionario(db, funcionario)

@router.get("/", response_model=List[FuncionarioRead])
def get_all_funcionarios(db: Session = Depends(get_db)):
    return service_funcionario.get_all_funcionarios(db)

@router.get("/{id}", response_model=FuncionarioRead)
def get_funcionario_by_id(id: int, db: Session = Depends(get_db)):
    funcionario = service_funcionario.get_funcionario_by_id(db, id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario

@router.get("/email/{email}", response_model=FuncionarioRead)
def get_funcionario_by_email(email: str, db: Session = Depends(get_db)):
    funcionario = service_funcionario.get_funcionario_by_email(db, email)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario

@router.post("/login")
def login_funcionario(credentials: FuncionarioLogin, db: Session = Depends(get_db)):
    """Login simples que retorna os dados do funcionário se as credenciais estiverem corretas"""
    funcionario = service_funcionario.authenticate_funcionario(db, credentials.email, credentials.senha)
    if not funcionario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    return {
        "success": True,
        "message": f"Login realizado com sucesso para o funcionário: {funcionario.nome}",
        "funcionario": {
            "id": funcionario.id,
            "nome": funcionario.nome,
            "email": funcionario.email,
            "cargo": funcionario.cargo
        }
    }

@router.put("/{id}", response_model=FuncionarioRead)
def update_funcionario(id: int, funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    return service_funcionario.update_funcionario(db, id, funcionario)

@router.delete("/{id}")
def delete_funcionario(id: int, db: Session = Depends(get_db)):
    return service_funcionario.delete_funcionario(db, id)
