from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.CuidadoPessoal.model_cuidado_pessoal import CuidadoPessoal
from app.SubcategoriaCuidadoPessoal.model_subcategoria_cuidado_pessoal import SubcategoriaCuidadoPessoal
from app.CuidadoPessoal.schema_cuidado_pessoal import CuidadoPessoalCreate

def create_cuidado_pessoal(db: Session, cuidado: CuidadoPessoalCreate):
    # Verifica se a subcategoria existe
    if cuidado.subcategoria_id:
        subcategoria = db.query(SubcategoriaCuidadoPessoal).filter(
            SubcategoriaCuidadoPessoal.id == cuidado.subcategoria_id
        ).first()
        if not subcategoria:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subcategoria não encontrada"
            )

    db_cuidado = CuidadoPessoal(**cuidado.dict())
    db.add(db_cuidado)
    db.commit()
    db.refresh(db_cuidado)
    return db_cuidado

def get_all_cuidados_pessoais(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CuidadoPessoal).offset(skip).limit(limit).all()

def get_cuidado_pessoal_by_id(db: Session, id: int):
    cuidado = db.query(CuidadoPessoal).filter(CuidadoPessoal.id == id).first()
    if not cuidado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto de cuidado pessoal não encontrado"
        )
    return cuidado

def get_cuidados_by_subcategoria(db: Session, subcategoria_id: int):
    return db.query(CuidadoPessoal).filter(
        CuidadoPessoal.subcategoria_id == subcategoria_id
    ).all()

def update_cuidado_pessoal(db: Session, id: int, cuidado: CuidadoPessoalCreate):
    db_cuidado = get_cuidado_pessoal_by_id(db, id)
    
    # Verifica se a nova subcategoria existe
    if cuidado.subcategoria_id and cuidado.subcategoria_id != db_cuidado.subcategoria_id:
        subcategoria = db.query(SubcategoriaCuidadoPessoal).filter(
            SubcategoriaCuidadoPessoal.id == cuidado.subcategoria_id
        ).first()
        if not subcategoria:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subcategoria não encontrada"
            )

    for field, value in cuidado.dict().items():
        setattr(db_cuidado, field, value)
    
    db.commit()
    db.refresh(db_cuidado)
    return db_cuidado

def delete_cuidado_pessoal(db: Session, id: int):
    db_cuidado = get_cuidado_pessoal_by_id(db, id)
    db.delete(db_cuidado)
    db.commit()
    return {"message": "Produto de cuidado pessoal removido com sucesso"}