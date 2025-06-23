from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.settings import SessionLocal
from app.schemas.fornecedor_schema import FornecedorCreate, FornecedorRead
from app.services import fornecedor_service

router = APIRouter(prefix="/fornecedores", tags=["Fornecedores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=FornecedorRead)
def create_fornecedor(fornecedor: FornecedorCreate, db: Session = Depends(get_db)):
    return fornecedor_service.create_fornecedor(db, fornecedor)

@router.get("/", response_model=List[FornecedorRead])
def get_all_fornecedores(db: Session = Depends(get_db)):
    return fornecedor_service.get_all_fornecedores(db)

@router.get("/{id}", response_model=FornecedorRead)
def get_fornecedor_by_id(id: int, db: Session = Depends(get_db)):
    fornecedor = fornecedor_service.get_fornecedor_by_id(db, id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return fornecedor

@router.get("/cnpj/{cnpj}", response_model=FornecedorRead)
def get_fornecedor_by_cnpj(cnpj: str, db: Session = Depends(get_db)):
    fornecedor = fornecedor_service.get_fornecedor_by_cnpj(db, cnpj)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return fornecedor

@router.put("/{id}", response_model=FornecedorRead)
def update_fornecedor(id: int, fornecedor: FornecedorCreate, db: Session = Depends(get_db)):
    return fornecedor_service.update_fornecedor(db, id, fornecedor)

@router.delete("/{id}")
def delete_fornecedor(id: int, db: Session = Depends(get_db)):
    return fornecedor_service.delete_fornecedor(db, id)
