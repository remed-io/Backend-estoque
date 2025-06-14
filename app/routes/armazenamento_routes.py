# app/api/armazenamento_endpoint.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.settings import SessionLocal
from app.schemas.armazenamento_schema import ArmazenamentoCreate, ArmazenamentoRead
from app.services import armazenamento_service

router = APIRouter(prefix="/remedioarmazenamentos", tags=["Armazenamentos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ArmazenamentoRead)
def create_armazenamento(armazenamento: ArmazenamentoCreate, db: Session = Depends(get_db)):
    return armazenamento_service.create_armazenamento(db, armazenamento)

@router.get("/", response_model=List[ArmazenamentoRead])
def get_all_armazenamentos(db: Session = Depends(get_db)):
    return armazenamento_service.get_all_armazenamentos(db)

@router.get("/{id}", response_model=ArmazenamentoRead)
def get_armazenamento_by_id(id: int, db: Session = Depends(get_db)):
    armazenamento = armazenamento_service.get_armazenamento_by_id(db, id)
    if not armazenamento:
        raise HTTPException(status_code=404, detail="Armazenamento não encontrado")
    return armazenamento

@router.put("/{id}", response_model=ArmazenamentoRead)
def update_armazenamento(id: int, armazenamento: ArmazenamentoCreate, db: Session = Depends(get_db)):
    return armazenamento_service.update_armazenamento(db, id, armazenamento)

@router.delete("/{id}")
def delete_armazenamento(id: int, db: Session = Depends(get_db)):
    return armazenamento_service.delete_armazenamento(db, id)
