from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.RestricaoAlimentar.model_restricao_alimentar import RestricaoAlimentar
from app.RestricaoAlimentar.schema_restricao_alimentar import RestricaoAlimentarCreate

def create_restricao_alimentar(db: Session, restricao: RestricaoAlimentarCreate):
    # Verifica se nome já existe
    existing = db.query(RestricaoAlimentar).filter(RestricaoAlimentar.nome == restricao.nome).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Restrição alimentar com nome '{restricao.nome}' já existe"
        )
    
    db_restricao = RestricaoAlimentar(**restricao.dict())
    db.add(db_restricao)
    db.commit()
    db.refresh(db_restricao)
    return db_restricao

def get_all_restricoes_alimentares(db: Session):
    return db.query(RestricaoAlimentar).all()

def get_restricao_alimentar_by_id(db: Session, id: int):
    return db.query(RestricaoAlimentar).filter(RestricaoAlimentar.id == id).first()

def get_restricao_alimentar_by_nome(db: Session, nome: str):
    return db.query(RestricaoAlimentar).filter(RestricaoAlimentar.nome == nome).first()

def update_restricao_alimentar(db: Session, id: int, restricao: RestricaoAlimentarCreate):
    db_restricao = db.query(RestricaoAlimentar).filter(RestricaoAlimentar.id == id).first()
    if not db_restricao:
        raise HTTPException(status_code=404, detail="Restrição alimentar não encontrada")
    
    if restricao.nome != db_restricao.nome:
        existing = db.query(RestricaoAlimentar).filter(RestricaoAlimentar.nome == restricao.nome).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Restrição alimentar com nome '{restricao.nome}' já existe"
            )
    
    db_restricao.nome = restricao.nome
    db.commit()
    db.refresh(db_restricao)
    return db_restricao

def delete_restricao_alimentar(db: Session, id: int):
    db_restricao = db.query(RestricaoAlimentar).filter(RestricaoAlimentar.id == id).first()
    if not db_restricao:
        raise HTTPException(status_code=404, detail="Restrição alimentar não encontrada")
    
    db.delete(db_restricao)
    db.commit()
    return {"message": "Restrição alimentar removida com sucesso"}