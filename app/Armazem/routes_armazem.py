# app/api/armazem_endpoint.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.settings import SessionLocal
from app.Armazem.schema_armazem import ArmazemCreate, ArmazemRead
from app.Armazem import service_armazem

router = APIRouter(prefix="/armazem", tags=["Armazém"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ArmazemRead)
def create_armazem(armazem: ArmazemCreate, db: Session = Depends(get_db)):
    return service_armazem.create_armazem(db, armazem)

@router.get("/", response_model=List[ArmazemRead])
def get_all_armazems(db: Session = Depends(get_db)):
    return service_armazem.get_all_armazems(db)

@router.get("/{id}", response_model=ArmazemRead)
def get_armazem_by_id(id: int, db: Session = Depends(get_db)):
    armazem = service_armazem.get_armazem_by_id(db, id)
    if not armazem:
        raise HTTPException(status_code=404, detail="Armazem não encontrado")
    return armazem

@router.put("/{id}", response_model=ArmazemRead)
def update_armazem(id: int, armazem: ArmazemCreate, db: Session = Depends(get_db)):
    return service_armazem.update_armazem(db, id, armazem)

@router.delete("/{id}")
def delete_armazem(id: int, db: Session = Depends(get_db)):
    return service_armazem.delete_armazem(db, id)
