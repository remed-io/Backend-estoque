from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.SubcategoriaCuidadePessoal.model_subcategoriacuidadopessoal import SubcategoriaCuidadePessoal
from app.SubcategoriaCuidadePessoal.schema_subcategoriacuidadopessoal import SubcategoriaCuidadePessoalCreate

def create_subcategoriacuidadopessoal(db: Session, subcategoria: SubcategoriaCuidadePessoalCreate):
    db_subcategoria = SubcategoriaCuidadePessoal(**subcategoria.dict())
    db.add(db_subcategoria)
    db.commit()
    db.refresh(db_subcategoria)
    return db_subcategoria

def get_all_subcategorias(db: Session):
    return db.query(SubcategoriaCuidadePessoal).all()

def get_subcategoria_by_id(db: Session, id: int):
    return db.query(SubcategoriaCuidadePessoal).filter(SubcategoriaCuidadePessoal.id == id).first()

def update_subcategoria(db: Session, id: int, subcategoria: SubcategoriaCuidadePessoalCreate):
    db_subcategoria = db.query(SubcategoriaCuidadePessoal).filter(SubcategoriaCuidadePessoal.id == id).first()
    if not db_subcategoria:
        raise HTTPException(status_code=404, detail="Subcategoria não encontrada")
    for key, value in subcategoria.dict().items():
        setattr(db_subcategoria, key, value)
    db.commit()
    db.refresh(db_subcategoria)
    return db_subcategoria

def delete_subcategoria(db: Session, id: int):
    db_subcategoria = db.query(SubcategoriaCuidadePessoal).filter(SubcategoriaCuidadePessoal.id == id).first()
    if not db_subcategoria:
        raise HTTPException(status_code=404, detail="Subcategoria não encontrada")
    db.delete(db_subcategoria)
    db.commit()
    return {"message": "Subcategoria deletada com sucesso"}
