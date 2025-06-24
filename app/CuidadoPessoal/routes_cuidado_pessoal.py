from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.settings import SessionLocal
from app.CuidadoPessoal.schema_cuidado_pessoal import CuidadoPessoalCreate, CuidadoPessoalRead
from app.CuidadoPessoal import service_cuidado_pessoal

router = APIRouter(prefix="/cuidado-pessoal", tags=["Cuidado Pessoal"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/", response_model=CuidadoPessoalRead)
def create_cuidado_pessoal(cuidado_pessoal: CuidadoPessoalCreate, db: Session = Depends(get_db)):
    return service_cuidado_pessoal.create_cuidado_pessoal(db, cuidado_pessoal)  

@router.get("/", response_model=List[CuidadoPessoalRead])
def get_all_cuidados_pessoais(db: Session = Depends(get_db)):
    return service_cuidado_pessoal.get_all_cuidados_pessoais(db)

@router.get("/{id}", response_model=CuidadoPessoalRead)
def get_cuidado_pessoal_by_id(id: int, db: Session = Depends(get_db)):
    cuidado_pessoal = service_cuidado_pessoal.get_cuidado_pessoal_by_id(db, id)
    if not cuidado_pessoal:
        raise HTTPException(status_code=404, detail="Cuidado Pessoal não encontrado")
    return cuidado_pessoal

#buscar a partir do nome
@router.get("/nome/{nome}", response_model=CuidadoPessoalRead)
def get_cuidado_pessoal_by_nome(nome: str, db: Session = Depends(get_db)):
    cuidado_pessoal = service_cuidado_pessoal.get_cuidado_pessoal_by_nome(db, nome)
    if not cuidado_pessoal:
        raise HTTPException(status_code=404, detail="Cuidado Pessoal não encontrado")
    return cuidado_pessoal  

#buscar a partir do nome da subcategoria
@router.get("/subcategoria/{subcategoria_nome}", response_model=List[CuidadoPessoalRead])
def get_cuidados_pessoais_by_subcategoria(subcategoria_nome: str, db: Session = Depends(get_db)):
    cuidados_pessoais = service_cuidado_pessoal.get_cuidados_pessoais_by_subcategoria(db, subcategoria_nome)
    if not cuidados_pessoais:
        raise HTTPException(status_code=404, detail="Nenhum Cuidado Pessoal encontrado para esta subcategoria")
    return cuidados_pessoais    

@router.put("/{id}", response_model=CuidadoPessoalRead)
def update_cuidado_pessoal(id: int, cuidado_pessoal: CuidadoPessoalCreate, db: Session = Depends(get_db)):
    updated_cuidado_pessoal = service_cuidado_pessoal.update_cuidado_pessoal(db, id, cuidado_pessoal)
    if not updated_cuidado_pessoal:
        raise HTTPException(status_code=404, detail="Cuidado Pessoal não encontrado")
    return updated_cuidado_pessoal

@router.delete("/{id}")
def delete_cuidado_pessoal(id: int, db: Session = Depends(get_db)):
    deleted = service_cuidado_pessoal.delete_cuidado_pessoal(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cuidado Pessoal não encontrado")
    return {"detail": "Cuidado Pessoal deletado com sucesso"}   


     