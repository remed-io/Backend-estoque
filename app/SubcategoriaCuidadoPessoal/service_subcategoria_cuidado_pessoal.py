from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.SubcategoriaCuidadoPessoal.model_subcategoria_cuidado_pessoal import SubcategoriaCuidadoPessoal
from app.SubcategoriaCuidadoPessoal.schema_subcategoria_cuidado_pessoal import SubcategoriaCuidadoPessoalCreate

def create_subcategoriacuidadopessoal(db: Session, subcategoria: SubcategoriaCuidadoPessoalCreate):
    db_subcategoria = SubcategoriaCuidadoPessoal(**subcategoria.dict())
    db.add(db_subcategoria)
    db.commit()
    db.refresh(db_subcategoria)
    return db_subcategoria

def get_all_subcategorias(db: Session):
    return db.query(SubcategoriaCuidadoPessoal).all()

def get_subcategoria_by_id(db: Session, id: int):
    return db.query(SubcategoriaCuidadoPessoal).filter(SubcategoriaCuidadoPessoal.id == id).first()

def update_subcategoria(db: Session, id: int, subcategoria: SubcategoriaCuidadoPessoalCreate):
    db_subcategoria = db.query(SubcategoriaCuidadoPessoal).filter(SubcategoriaCuidadoPessoal.id == id).first()
    if not db_subcategoria:
        raise HTTPException(status_code=404, detail="Subcategoria não encontrada")
    for key, value in subcategoria.dict().items():
        setattr(db_subcategoria, key, value)
    db.commit()
    db.refresh(db_subcategoria)
    return db_subcategoria

def delete_subcategoria(db: Session, id: int):
    db_subcategoria = db.query(SubcategoriaCuidadoPessoal).filter(SubcategoriaCuidadoPessoal.id == id).first()
    if not db_subcategoria:
        raise HTTPException(status_code=404, detail="Subcategoria não encontrada")
    db.delete(db_subcategoria)
    db.commit()
    return {"message": "Subcategoria deletada com sucesso"}
