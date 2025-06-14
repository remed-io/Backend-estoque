# app/api/funcionario_endpoint.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.settings import SessionLocal
from app.schemas.funcionario_schema import (
    FuncionarioCreate,
    FuncionarioRead,
    FuncionarioLogin
)
from app.services import funcionario_service

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=FuncionarioRead)
def create_funcionario(funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    return funcionario_service.create_funcionario(db, funcionario)

@router.get("/", response_model=List[FuncionarioRead])
def get_all_funcionarios(db: Session = Depends(get_db)):
    return funcionario_service.get_all_funcionarios(db)

@router.get("/{id}", response_model=FuncionarioRead)
def get_funcionario_by_id(id: int, db: Session = Depends(get_db)):
    funcionario = funcionario_service.get_funcionario_by_id(db, id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario

@router.get("/email/{email}", response_model=FuncionarioRead)
def get_funcionario_by_email(email: str, db: Session = Depends(get_db)):
    funcionario = funcionario_service.get_funcionario_by_email(db, email)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario

@router.post("/login", response_model=FuncionarioRead)
def login_funcionario(credentials: FuncionarioLogin, db: Session = Depends(get_db)):
    funcionario = funcionario_service.authenticate_funcionario(db, credentials.email, credentials.senha)
    if not funcionario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    return funcionario

@router.put("/{id}", response_model=FuncionarioRead)
def update_funcionario(id: int, funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    return funcionario_service.update_funcionario(db, id, funcionario)

@router.delete("/{id}")
def delete_funcionario(id: int, db: Session = Depends(get_db)):
    return funcionario_service.delete_funcionario(db, id)
