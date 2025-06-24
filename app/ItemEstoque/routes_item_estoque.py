from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.settings import SessionLocal
from app.ItemEstoque.schema_item_estoque import ItemEstoqueCreate, ItemEstoqueRead
from app.ItemEstoque import service_item_estoque

router = APIRouter(prefix="/item-estoque", tags=["Item Estoque"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ItemEstoqueRead)
def create_item(item: ItemEstoqueCreate, db: Session = Depends(get_db)):
    return service_item_estoque.create_itemestoque(db, item)

@router.get("/", response_model=List[ItemEstoqueRead])
def get_all_itens(db: Session = Depends(get_db)):
    return service_item_estoque.get_all_itens(db)

@router.get("/{id}", response_model=ItemEstoqueRead)
def get_item_by_id(id: int, db: Session = Depends(get_db)):
    item = service_item_estoque.get_item_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item

@router.put("/{id}", response_model=ItemEstoqueRead)
def update_item(id: int, item: ItemEstoqueCreate, db: Session = Depends(get_db)):
    return service_item_estoque.update_item(db, id, item)

@router.delete("/{id}")
def delete_item(id: int, db: Session = Depends(get_db)):
    return service_item_estoque.delete_item(db, id)
