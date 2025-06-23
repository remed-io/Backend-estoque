from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.ItemEstoque.model_item_estoque import ItemEstoque
from app.ItemEstoque.schema_item_estoque import ItemEstoqueCreate

def create_itemestoque(db: Session, item: ItemEstoqueCreate):
    db_item = ItemEstoque(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_all_itens(db: Session):
    return db.query(ItemEstoque).all()

def get_item_by_id(db: Session, id: int):
    return db.query(ItemEstoque).filter(ItemEstoque.id == id).first()

def update_item(db: Session, id: int, item: ItemEstoqueCreate):
    db_item = db.query(ItemEstoque).filter(ItemEstoque.id == id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, id: int):
    db_item = db.query(ItemEstoque).filter(ItemEstoque.id == id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deletado com sucesso"}
