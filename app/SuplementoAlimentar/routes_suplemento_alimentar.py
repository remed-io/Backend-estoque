from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.settings import get_db
from app.SuplementoAlimentar.schema_suplemento_alimentar import SuplementoAlimentarCreate, SuplementoAlimentarRead
from app.SuplementoAlimentar import service_suplemento_alimentar

router = APIRouter(prefix="/suplemento-alimentar", tags=["SuplementoAlimentar"])

@router.post("/", response_model=SuplementoAlimentarRead)
def create_suplemento(suplemento: SuplementoAlimentarCreate, db: Session = Depends(get_db)):
    return service_suplemento_alimentar.create_suplemento(db, suplemento)

@router.get("/", response_model=List[SuplementoAlimentarRead])
def get_all_suplementos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service_suplemento_alimentar.get_all_suplementos(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=SuplementoAlimentarRead)
def get_suplemento_by_id(id: int, db: Session = Depends(get_db)):
    return service_suplemento_alimentar.get_suplemento_by_id(db, id)

@router.get("/search/", response_model=List[SuplementoAlimentarRead])
def search_suplementos(query: str, db: Session = Depends(get_db)):
    return service_suplemento_alimentar.search_suplementos(db, query)

@router.put("/{id}", response_model=SuplementoAlimentarRead)
def update_suplemento(id: int, suplemento: SuplementoAlimentarCreate, db: Session = Depends(get_db)):
    return service_suplemento_alimentar.update_suplemento(db, id, suplemento)

@router.delete("/{id}")
def delete_suplemento(id: int, db: Session = Depends(get_db)):
    return service_suplemento_alimentar.delete_suplemento(db, id)
