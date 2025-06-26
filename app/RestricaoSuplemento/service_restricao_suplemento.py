from sqlalchemy.orm import Session
from app.RestricaoSuplemento.model_restricao_suplemento import RestricaoSuplemento
from app.RestricaoSuplemento.schema_restricao_suplemento import RestricaoSuplementoCreate

def criar_restricao_suplemento(db: Session, item: RestricaoSuplementoCreate):
    db_item = RestricaoSuplemento(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def listar_restricoes_suplemento(db: Session):
    return db.query(RestricaoSuplemento).all() 