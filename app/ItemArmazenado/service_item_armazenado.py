from sqlalchemy.orm import Session
from app.ItemArmazenado.model_item_armazenado import ItemArmazenado
from app.ItemArmazenado.schema_item_armazenado import ItemArmazenadoCreate
from datetime import datetime

def criar_item_armazenado(db: Session, item: ItemArmazenadoCreate):
    db_item = ItemArmazenado(
        armazem_id=item.armazem_id,
        item_estoque_id=item.item_estoque_id,
        quantidade=item.quantidade,
        data_atualizacao=datetime.now()
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def listar_itens_armazenados(db: Session):
    return db.query(ItemArmazenado).all() 