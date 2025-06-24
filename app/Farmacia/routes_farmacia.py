from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.settings import SessionLocal
from app.Farmacia.schema_farmacia import FarmaciaCreate, FarmaciaRead
from app.Farmacia import service_farmacia

router = APIRouter(prefix="/farmacia", tags=["Farmácia"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=FarmaciaRead)
def create_farmacia(farmacia: FarmaciaCreate, db: Session = Depends(get_db)):
    return service_farmacia.create_farmacia(db, farmacia)

@router.get("/", response_model=List[FarmaciaRead])
def get_all_farmacias(db: Session = Depends(get_db)):
    return service_farmacia.get_all_farmacias(db)

@router.get("/{id}", response_model=FarmaciaRead)
def get_farmacia_by_id(id: int, db: Session = Depends(get_db)):
    farmacia = service_farmacia.get_farmacia_by_id(db, id)
    if not farmacia:
        raise HTTPException(status_code=404, detail="Farmacia não encontrada")
    return farmacia

@router.put("/{id}", response_model=FarmaciaRead)
def update_farmacia(id: int, farmacia: FarmaciaCreate, db: Session = Depends(get_db)):
    return service_farmacia.update_farmacia(db, id, farmacia)

@router.delete("/{id}")
def delete_farmacia(id: int, db: Session = Depends(get_db)):
    return service_farmacia.delete_farmacia(db, id)
