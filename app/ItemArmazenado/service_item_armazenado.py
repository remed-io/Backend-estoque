from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.ItemArmazenado.model_item_armazenado import ItemArmazenado
from app.ItemArmazenado.schema_item_armazenado import ItemArmazenadoCreate
from datetime import datetime

def criar_item_armazenado(db: Session, item: ItemArmazenadoCreate):
    # Verificar se já existe um item neste armazém
    existing_item = db.query(ItemArmazenado).filter(
        ItemArmazenado.armazem_id == item.armazem_id,
        ItemArmazenado.item_estoque_id == item.item_estoque_id
    ).first()
    
    if existing_item:
        # Se já existe, atualizar a quantidade
        existing_item.quantidade += item.quantidade
        existing_item.data_atualizacao = datetime.now()
        db.commit()
        db.refresh(existing_item)
        return existing_item
    
    # Se não existe, criar novo
    db_item = ItemArmazenado(
        armazem_id=item.armazem_id,
        item_estoque_id=item.item_estoque_id,
        quantidade=item.quantidade,
        data_atualizacao=datetime.now()
    )
    
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail=f"Erro ao armazenar item: {str(e)}"
        )

def listar_itens_armazenados(db: Session):
    return db.query(ItemArmazenado).all() 