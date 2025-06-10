# app/services/medicamento_service.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.medicamento import Medicamento
from app.schemas.medicamento_schema import MedicamentoCreate

def create_medicamento(db: Session, medicamento: MedicamentoCreate):
    db_medicamento = Medicamento(**medicamento.dict())
    db.add(db_medicamento)
    db.commit()
    db.refresh(db_medicamento)
    return db_medicamento

def get_all_medicamentos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Medicamento).offset(skip).limit(limit).all()

def get_medicamento_by_id(db: Session, id: int):
    medicamento = db.query(Medicamento).filter(Medicamento.id == id).first()
    if not medicamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicamento não encontrado"
        )
    return medicamento

def search_medicamentos(db: Session, query: str, skip: int = 0, limit: int = 100):
    return db.query(Medicamento).filter(
        Medicamento.nome.ilike(f"%{query}%") |
        Medicamento.principio_ativo.ilike(f"%{query}%") |
        Medicamento.fabricante.ilike(f"%{query}%")
    ).offset(skip).limit(limit).all()

def update_medicamento(db: Session, id: int, medicamento: MedicamentoCreate):
    db_medicamento = get_medicamento_by_id(db, id)
    
    for field, value in medicamento.dict().items():
        setattr(db_medicamento, field, value)
    
    db.commit()
    db.refresh(db_medicamento)
    return db_medicamento

def delete_medicamento(db: Session, id: int):
    db_medicamento = get_medicamento_by_id(db, id)
    db.delete(db_medicamento)
    db.commit()
    return {"message": "Medicamento removido com sucesso"}