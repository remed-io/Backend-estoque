from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.ItemEstoque.model_item_estoque import ItemEstoque
from app.ItemEstoque.schema_item_estoque import ItemEstoqueCreate
from app.Medicamento.model_medicamento import Medicamento
from app.CuidadoPessoal.model_cuidado_pessoal import CuidadoPessoal
from app.SuplementoAlimentar.model_suplemento_alimentar import SuplementoAlimentar
import logging

def create_itemestoque(db: Session, item: ItemEstoqueCreate):
    # Verifica se já existe código de barras
    if db.query(ItemEstoque).filter(ItemEstoque.codigo_barras == item.codigo_barras).first():
        logging.error(f"Tentativa de cadastro de código de barras duplicado: {item.codigo_barras}")
        raise HTTPException(status_code=400, detail="Código de barras já cadastrado")
    produto_id = None
    produto_nome = None
    tipo_produto = None

    if item.produto_medicamento_id:
        tipo_produto = "medicamento"
        produto = db.query(Medicamento).filter(Medicamento.id == item.produto_medicamento_id).first()
        if not produto:
            raise HTTPException(status_code=400, detail="Medicamento não encontrado")
        produto_id = produto.id
        produto_nome = produto.nome
    elif item.produto_cuidado_pessoal_id:
        tipo_produto = "cuidado_pessoal"
        produto = db.query(CuidadoPessoal).filter(CuidadoPessoal.id == item.produto_cuidado_pessoal_id).first()
        if not produto:
            raise HTTPException(status_code=400, detail="Cuidado Pessoal não encontrado")
        produto_id = produto.id
        produto_nome = produto.nome
    elif item.produto_suplemento_alimentar_id:
        tipo_produto = "suplemento_alimentar"
        produto = db.query(SuplementoAlimentar).filter(SuplementoAlimentar.id == item.produto_suplemento_alimentar_id).first()
        if not produto:
            raise HTTPException(status_code=400, detail="Suplemento Alimentar não encontrado")
        produto_id = produto.id
        produto_nome = produto.nome
    else:
        raise HTTPException(status_code=400, detail="É necessário informar um produto válido.")

    data = item.dict().copy()
    data.pop("produto_id", None)
    data.pop("produto_nome", None)
    data.pop("tipo_produto", None)
    db_item = ItemEstoque(**data, produto_id=produto_id, produto_nome=produto_nome, tipo_produto=tipo_produto)
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

    produto_id = None
    produto_nome = None
    tipo_produto = None

    if item.produto_medicamento_id:
        tipo_produto = "medicamento"
        produto = db.query(Medicamento).filter(Medicamento.id == item.produto_medicamento_id).first()
        if not produto:
            raise HTTPException(status_code=400, detail="Medicamento não encontrado")
        produto_id = produto.id
        produto_nome = produto.nome
    elif item.produto_cuidado_pessoal_id:
        tipo_produto = "cuidado_pessoal"
        produto = db.query(CuidadoPessoal).filter(CuidadoPessoal.id == item.produto_cuidado_pessoal_id).first()
        if not produto:
            raise HTTPException(status_code=400, detail="Cuidado Pessoal não encontrado")
        produto_id = produto.id
        produto_nome = produto.nome
    elif item.produto_suplemento_alimentar_id:
        tipo_produto = "suplemento_alimentar"
        produto = db.query(SuplementoAlimentar).filter(SuplementoAlimentar.id == item.produto_suplemento_alimentar_id).first()
        if not produto:
            raise HTTPException(status_code=400, detail="Suplemento Alimentar não encontrado")
        produto_id = produto.id
        produto_nome = produto.nome
    else:
        raise HTTPException(status_code=400, detail="É necessário informar um produto válido.")

    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db_item.produto_id = produto_id
    db_item.produto_nome = produto_nome
    db_item.tipo_produto = tipo_produto
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
