# app/services/suplemento_alimentar_service.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.suplemento_alimentar import SuplementoAlimentar
from app.schemas.suplemento_alimentar_schema import SuplementoAlimentarCreate

def create_suplemento(db: Session, suplemento: SuplementoAlimentarCreate):
    db_suplemento = SuplementoAlimentar(**suplemento.dict())
    db.add(db_suplemento)
    db.commit()
    db.refresh(db_suplemento)
    return db_suplemento

def get_all_suplementos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SuplementoAlimentar).offset(skip).limit(limit).all()

def get_suplemento_by_id(db: Session, id: int):
    suplemento = db.query(SuplementoAlimentar).filter(SuplementoAlimentar.id == id).first()
    if not suplemento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Suplemento não encontrado"
        )
    return suplemento

def search_suplementos(db: Session, query: str):
    return db.query(SuplementoAlimentar).filter(
        SuplementoAlimentar.nome.ilike(f"%{query}%") |
        SuplementoAlimentar.principio_ativo.ilike(f"%{query}%") |
        SuplementoAlimentar.fabricante.ilike(f"%{query}%")
    ).all()

def update_suplemento(db: Session, id: int, suplemento: SuplementoAlimentarCreate):
    db_suplemento = get_suplemento_by_id(db, id)
    
    for field, value in suplemento.dict().items():
        setattr(db_suplemento, field, value)
    
    db.commit()
    db.refresh(db_suplemento)
    return db_suplemento

def delete_suplemento(db: Session, id: int):
    db_suplemento = get_suplemento_by_id(db, id)
    db.delete(db_suplemento)
    db.commit()
    return {"message": "Suplemento removido com sucesso"}