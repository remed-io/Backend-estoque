#app/service/restricao_service.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.restricao import Restricao
from app.schemas.restricao_schema import RestricaoCreate

def create_restricao(db: Session, restricao: RestricaoCreate):
    # Verifica se nome já existe
    existing = db.query(Restricao).filter(Restricao.nome == restricao.nome).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Restrição com nome '{restricao.nome}' já existe"
        )
    
    db_restricao = Restricao(**restricao.dict())
    db.add(db_restricao)
    db.commit()
    db.refresh(db_restricao)
    return db_restricao

def get_all_restricoes(db: Session):
    return db.query(Restricao).all()

def get_restricao_by_id(db: Session, id: int):
    return db.query(Restricao).filter(Restricao.id == id).first()

def get_restricao_by_nome(db: Session, nome: str):
    return db.query(Restricao).filter(Restricao.nome == nome).first()

def update_restricao(db: Session, id: int, restricao: RestricaoCreate):
    db_restricao = db.query(Restricao).filter(Restricao.id == id).first()
    if not db_restricao:
        raise HTTPException(status_code=404, detail="Restrição não encontrada")
    
    if restricao.nome != db_restricao.nome:
        existing = db.query(Restricao).filter(Restricao.nome == restricao.nome).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Restrição com nome '{restricao.nome}' já existe"
            )
    
    db_restricao.nome = restricao.nome
    db.commit()
    db.refresh(db_restricao)
    return db_restricao

def delete_restricao(db: Session, id: int):
    db_restricao = db.query(Restricao).filter(Restricao.id == id).first()
    if not db_restricao:
        raise HTTPException(status_code=404, detail="Restrição não encontrada")
    
    db.delete(db_restricao)
    db.commit()
    return {"message": "Restrição removida com sucesso"}