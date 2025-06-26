from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.settings import get_db
from app.Fornecedor.schema_fornecedor import FornecedorCreate, FornecedorRead
from app.Fornecedor import service_fornecedor

router = APIRouter( prefix="/fornecedor", tags=["Fornecedor"])

@router.post("/", response_model=FornecedorRead)
def create_fornecedor(fornecedor: FornecedorCreate, db: Session = Depends(get_db)):
    return service_fornecedor.create_fornecedor(db, fornecedor)

@router.get("/", response_model=List[FornecedorRead])
def get_all_fornecedores(db: Session = Depends(get_db)):
    return service_fornecedor.get_all_fornecedores(db)

@router.get("/{id}", response_model=FornecedorRead)
def get_fornecedor_by_id(id: int, db: Session = Depends(get_db)):
    fornecedor = service_fornecedor.get_fornecedor_by_id(db, id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return fornecedor

@router.get("/cnpj/{cnpj}", response_model=FornecedorRead)
def get_fornecedor_by_cnpj(cnpj: str, db: Session = Depends(get_db)):
    fornecedor = service_fornecedor.get_fornecedor_by_cnpj(db, cnpj)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return fornecedor

@router.put("/{id}", response_model=FornecedorRead)
def update_fornecedor(id: int, fornecedor: FornecedorCreate, db: Session = Depends(get_db)):
    return service_fornecedor.update_fornecedor(db, id, fornecedor)

@router.delete("/{id}")
def delete_fornecedor(id: int, db: Session = Depends(get_db)):
    return service_fornecedor.delete_fornecedor(db, id)
