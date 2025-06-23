from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.settings import SessionLocal
from app.SubcategoriaCuidadePessoal.schema_subcategoriacuidadopessoal import SubcategoriaCuidadePessoalCreate, SubcategoriaCuidadePessoalRead
from app.SubcategoriaCuidadePessoal import service_subcategoriacuidadopessoal

router = APIRouter(prefix="/subcategoriascuidadopessoal", tags=["SubcategoriasCuidadoPessoal"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SubcategoriaCuidadePessoalRead)
def create_subcategoria(subcategoria: SubcategoriaCuidadePessoalCreate, db: Session = Depends(get_db)):
    return service_subcategoriacuidadopessoal.create_subcategoriacuidadopessoal(db, subcategoria)

@router.get("/", response_model=List[SubcategoriaCuidadePessoalRead])
def get_all_subcategorias(db: Session = Depends(get_db)):
    return service_subcategoriacuidadopessoal.get_all_subcategorias(db)

@router.get("/{id}", response_model=SubcategoriaCuidadePessoalRead)
def get_subcategoria_by_id(id: int, db: Session = Depends(get_db)):
    subcategoria = service_subcategoriacuidadopessoal.get_subcategoria_by_id(db, id)
    if not subcategoria:
        raise HTTPException(status_code=404, detail="Subcategoria não encontrada")
    return subcategoria

@router.put("/{id}", response_model=SubcategoriaCuidadePessoalRead)
def update_subcategoria(id: int, subcategoria: SubcategoriaCuidadePessoalCreate, db: Session = Depends(get_db)):
    return service_subcategoriacuidadopessoal.update_subcategoria(db, id, subcategoria)

@router.delete("/{id}")
def delete_subcategoria(id: int, db: Session = Depends(get_db)):
    return service_subcategoriacuidadopessoal.delete_subcategoria(db, id)
