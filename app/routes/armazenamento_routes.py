# app/api/armazem_endpoint.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.settings import SessionLocal
from app.schemas.armazem_schema import ArmazemCreate, ArmazemRead
from app.services import armazem_service

router = APIRouter(prefix="/remedioarmazems", tags=["Armazems"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ArmazemRead)
def create_armazem(armazem: ArmazemCreate, db: Session = Depends(get_db)):
    return armazem_service.create_armazem(db, armazem)

@router.get("/", response_model=List[ArmazemRead])
def get_all_armazems(db: Session = Depends(get_db)):
    return armazem_service.get_all_armazems(db)

@router.get("/{id}", response_model=ArmazemRead)
def get_armazem_by_id(id: int, db: Session = Depends(get_db)):
    armazem = armazem_service.get_armazem_by_id(db, id)
    if not armazem:
        raise HTTPException(status_code=404, detail="Armazem não encontrado")
    return armazem

@router.put("/{id}", response_model=ArmazemRead)
def update_armazem(id: int, armazem: ArmazemCreate, db: Session = Depends(get_db)):
    return armazem_service.update_armazem(db, id, armazem)

@router.delete("/{id}")
def delete_armazem(id: int, db: Session = Depends(get_db)):
    return armazem_service.delete_armazem(db, id)
