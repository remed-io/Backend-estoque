# app/api/restricao_endpoint.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.settings import SessionLocal
from app.schemas.restricao_schema import RestricaoCreate, RestricaoRead
from app.services import restricao_service

router = APIRouter(prefix="/restricoes", tags=["Restrições"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=RestricaoRead)
def create_restricao(restricao: RestricaoCreate, db: Session = Depends(get_db)):
    return restricao_service.create_restricao(db, restricao)

@router.get("/", response_model=List[RestricaoRead])
def get_all_restricoes(db: Session = Depends(get_db)):
    return restricao_service.get_all_restricoes(db)

@router.get("/{id}", response_model=RestricaoRead)
def get_restricao_by_id(id: int, db: Session = Depends(get_db)):
    restricao = restricao_service.get_restricao_by_id(db, id)
    if not restricao:
        raise HTTPException(status_code=404, detail="Restrição não encontrada")
    return restricao

@router.get("/nome/{nome}", response_model=RestricaoRead)
def get_restricao_by_nome(nome: str, db: Session = Depends(get_db)):
    restricao = restricao_service.get_restricao_by_nome(db, nome)
    if not restricao:
        raise HTTPException(status_code=404, detail="Restrição não encontrada")
    return restricao

@router.put("/{id}", response_model=RestricaoRead)
def update_restricao(id: int, restricao: RestricaoCreate, db: Session = Depends(get_db)):
    return restricao_service.update_restricao(db, id, restricao)

@router.delete("/{id}")
def delete_restricao(id: int, db: Session = Depends(get_db)):
    return restricao_service.delete_restricao(db, id)
