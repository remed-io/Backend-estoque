from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.Farmacia.model_farmacia import Farmacia
from app.Farmacia.schema_farmacia import FarmaciaCreate

def create_farmacia(db: Session, farmacia: FarmaciaCreate):
    db_farmacia = Farmacia()
    db.add(db_farmacia)
    db.commit()
    db.refresh(db_farmacia)
    return db_farmacia

def get_all_farmacias(db: Session):
    return db.query(Farmacia).all()

def get_farmacia_by_id(db: Session, id: int):
    return db.query(Farmacia).filter(Farmacia.id == id).first()

def update_farmacia(db: Session, id: int, farmacia: FarmaciaCreate):
    db_farmacia = db.query(Farmacia).filter(Farmacia.id == id).first()
    if not db_farmacia:
        raise HTTPException(status_code=404, detail="Farmacia não encontrada")
    db.commit()
    db.refresh(db_farmacia)
    return db_farmacia

def delete_farmacia(db: Session, id: int):
    db_farmacia = db.query(Farmacia).filter(Farmacia.id == id).first()
    if not db_farmacia:
        raise HTTPException(status_code=404, detail="Farmacia não encontrada")
    db.delete(db_farmacia)
    db.commit()
    return {"message": "Farmacia deletada com sucesso"}
