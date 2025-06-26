from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.settings import get_db
from app.ItemArmazenado.schema_item_armazenado import ItemArmazenadoCreate, ItemArmazenadoRead
from app.ItemArmazenado.service_item_armazenado import criar_item_armazenado, listar_itens_armazenados
from typing import List

router = APIRouter(prefix="/item_armazenado", tags=["ItemArmazenado"])

@router.post("/", response_model=ItemArmazenadoRead)
def criar(item: ItemArmazenadoCreate, db: Session = Depends(get_db)):
    return criar_item_armazenado(db, item)

@router.get("/", response_model=List[ItemArmazenadoRead])
def listar(db: Session = Depends(get_db)):
    return listar_itens_armazenados(db) 