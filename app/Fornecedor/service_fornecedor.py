from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.Fornecedor.model_fornecedor import Fornecedor
from app.Fornecedor.schema_fornecedor import FornecedorCreate

def create_fornecedor(db: Session, fornecedor: FornecedorCreate):
    # Verifica se CNPJ já existe
    existing = db.query(Fornecedor).filter(Fornecedor.cnpj == fornecedor.cnpj).first()
    if existing:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado")
    
    db_fornecedor = Fornecedor(**fornecedor.dict())
    db.add(db_fornecedor)
    db.commit()
    db.refresh(db_fornecedor)
    return db_fornecedor

def get_all_fornecedores(db: Session):
    return db.query(Fornecedor).all()

def get_fornecedor_by_id(db: Session, id: int):
    return db.query(Fornecedor).filter(Fornecedor.id == id).first()

def get_fornecedor_by_cnpj(db: Session, cnpj: str):
    return db.query(Fornecedor).filter(Fornecedor.cnpj == cnpj).first()

def update_fornecedor(db: Session, id: int, fornecedor: FornecedorCreate):
    db_fornecedor = db.query(Fornecedor).filter(Fornecedor.id == id).first()
    if not db_fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    
    # Verifica se novo CNPJ já pertence a outro fornecedor
    if fornecedor.cnpj != db_fornecedor.cnpj:
        existing = db.query(Fornecedor).filter(Fornecedor.cnpj == fornecedor.cnpj).first()
        if existing:
            raise HTTPException(status_code=400, detail="CNPJ já cadastrado para outro fornecedor")
        
    for key, value in fornecedor.dict().items():
        setattr(db_fornecedor, key, value)
    db.commit()
    db.refresh(db_fornecedor)
    return db_fornecedor

def delete_fornecedor(db: Session, id: int):
    db_fornecedor = db.query(Fornecedor).filter(Fornecedor.id == id).first()
    if not db_fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    db.delete(db_fornecedor)
    db.commit()
    return {"message": "Fornecedor deletado com sucesso"}
