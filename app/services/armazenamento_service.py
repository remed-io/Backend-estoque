#app/services/armazenamento_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.armazenamento import Armazenamento
from app.schemas.armazenamento_schema import ArmazenamentoCreate

def create_armazenamento(db: Session, armazenamento: ArmazenamentoCreate):
    db_armazenamento = Armazenamento(**armazenamento.dict())
    db.add(db_armazenamento)
    db.commit()
    db.refresh(db_armazenamento)
    return db_armazenamento

def get_all_armazenamentos(db: Session):
    return db.query(Armazenamento).all()

def get_armazenamento_by_id(db: Session, id: int):
    return db.query(Armazenamento).filter(Armazenamento.id == id).first()

def update_armazenamento(db: Session, id: int, armazenamento: ArmazenamentoCreate):
    db_armazenamento = db.query(Armazenamento).filter(Armazenamento.id == id).first()
    if not db_armazenamento:
        raise HTTPException(status_code=404, detail="Armazenamento não encontrado")
    for key, value in armazenamento.dict().items():
        setattr(db_armazenamento, key, value)
    db.commit()
    db.refresh(db_armazenamento)
    return db_armazenamento

def delete_armazenamento(db: Session, id: int):
    db_armazenamento = db.query(Armazenamento).filter(Armazenamento.id == id).first()
    if not db_armazenamento:
        raise HTTPException(status_code=404, detail="Armazenamento não encontrado")
    db.delete(db_armazenamento)
    db.commit()
    return {"message": "Armazenamento deletado com sucesso"}
