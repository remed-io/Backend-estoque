#app/services/subcategoria_cuidado_pessoal_service.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.subcategoria_cuidado_pessoal import SubcategoriaCuidadoPessoal
from app.schemas.subcategoria_cuidado_pessoal_schema import SubcategoriaCuidadoPessoalCreate

def create_subcategoria(db: Session, subcategoria: SubcategoriaCuidadoPessoalCreate):
    # Verifica se nome já existe
    existing = db.query(SubcategoriaCuidadoPessoal).filter(
        SubcategoriaCuidadoPessoal.nome == subcategoria.nome
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Subcategoria com nome '{subcategoria.nome}' já existe"
        )
    
    db_subcategoria = SubcategoriaCuidadoPessoal(**subcategoria.dict())
    db.add(db_subcategoria)
    db.commit()
    db.refresh(db_subcategoria)
    return db_subcategoria

def get_all_subcategorias(db: Session):
    return db.query(SubcategoriaCuidadoPessoal).all()

def get_subcategoria_by_id(db: Session, id: int):
    return db.query(SubcategoriaCuidadoPessoal).filter(
        SubcategoriaCuidadoPessoal.id == id
    ).first()

def get_subcategoria_by_nome(db: Session, nome: str):
    return db.query(SubcategoriaCuidadoPessoal).filter(
        SubcategoriaCuidadoPessoal.nome == nome
    ).first()

def update_subcategoria(db: Session, id: int, subcategoria: SubcategoriaCuidadoPessoalCreate):
    db_subcategoria = db.query(SubcategoriaCuidadoPessoal).filter(
        SubcategoriaCuidadoPessoal.id == id
    ).first()
    if not db_subcategoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subcategoria não encontrada"
        )
    
    # Verifica se novo nome já existe
    if subcategoria.nome != db_subcategoria.nome:
        existing = db.query(SubcategoriaCuidadoPessoal).filter(
            SubcategoriaCuidadoPessoal.nome == subcategoria.nome
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Subcategoria com nome '{subcategoria.nome}' já existe"
            )
    
    for key, value in subcategoria.dict().items():
        setattr(db_subcategoria, key, value)
    
    db.commit()
    db.refresh(db_subcategoria)
    return db_subcategoria

def delete_subcategoria(db: Session, id: int):
    db_subcategoria = db.query(SubcategoriaCuidadoPessoal).filter(
        SubcategoriaCuidadoPessoal.id == id
    ).first()
    if not db_subcategoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subcategoria não encontrada"
        )
    
    db.delete(db_subcategoria)
    db.commit()
    return {"message": "Subcategoria removida com sucesso"}