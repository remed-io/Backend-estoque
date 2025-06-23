#app/services/armazem_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.Armazem.model_armazem import Armazem
from app.Armazem.schema_armazem import ArmazemCreate

def create_armazem(db: Session, armazem: ArmazemCreate):
    db_armazem = Armazem(**armazem.dict())
    db.add(db_armazem)
    db.commit()
    db.refresh(db_armazem)
    return db_armazem

def get_all_armazems(db: Session):
    return db.query(Armazem).all()

def get_armazem_by_id(db: Session, id: int):
    return db.query(Armazem).filter(Armazem.id == id).first()

def update_armazem(db: Session, id: int, armazem: ArmazemCreate):
    db_armazem = db.query(Armazem).filter(Armazem.id == id).first()
    if not db_armazem:
        raise HTTPException(status_code=404, detail="Armazem não encontrado")
    for key, value in armazem.dict().items():
        setattr(db_armazem, key, value)
    db.commit()
    db.refresh(db_armazem)
    return db_armazem

def delete_armazem(db: Session, id: int):
    db_armazem = db.query(Armazem).filter(Armazem.id == id).first()
    if not db_armazem:
        raise HTTPException(status_code=404, detail="Armazem não encontrado")
    db.delete(db_armazem)
    db.commit()
    return {"message": "Armazem deletado com sucesso"}
