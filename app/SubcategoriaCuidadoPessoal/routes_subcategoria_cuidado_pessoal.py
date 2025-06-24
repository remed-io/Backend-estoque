from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.settings import get_db
from app.SubcategoriaCuidadoPessoal.schema_subcategoria_cuidado_pessoal import SubcategoriaCuidadoPessoalCreate, SubcategoriaCuidadoPessoalRead
from app.SubcategoriaCuidadoPessoal import service_subcategoria_cuidado_pessoal

router = APIRouter( prefix="/subcategoria-cuidado-pessoal", tags=["Subcategoria Cuidado Pessoal"])

@router.post("/", response_model=SubcategoriaCuidadoPessoalRead)
def create_subcategoria(subcategoria: SubcategoriaCuidadoPessoalCreate, db: Session = Depends(get_db)):
    return service_subcategoria_cuidado_pessoal.create_subcategoriacuidadopessoal(db, subcategoria)

@router.get("/", response_model=List[SubcategoriaCuidadoPessoalRead])
def get_all_subcategorias(db: Session = Depends(get_db)):
    return service_subcategoria_cuidado_pessoal.get_all_subcategorias(db)

@router.get("/{id}", response_model=SubcategoriaCuidadoPessoalRead)
def get_subcategoria_by_id(id: int, db: Session = Depends(get_db)):
    subcategoria = service_subcategoria_cuidado_pessoal.get_subcategoria_by_id(db, id)
    if not subcategoria:
        raise HTTPException(status_code=404, detail="Subcategoria não encontrada")
    return subcategoria

@router.put("/{id}", response_model=SubcategoriaCuidadoPessoalRead)
def update_subcategoria(id: int, subcategoria: SubcategoriaCuidadoPessoalCreate, db: Session = Depends(get_db)):
    return service_subcategoria_cuidado_pessoal.update_subcategoria(db, id, subcategoria)

@router.delete("/{id}")
def delete_subcategoria(id: int, db: Session = Depends(get_db)):
    return service_subcategoria_cuidado_pessoal.delete_subcategoria(db, id)
