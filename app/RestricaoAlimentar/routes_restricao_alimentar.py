from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.settings import get_db
from app.RestricaoAlimentar.schema_restricao_alimentar import RestricaoAlimentarCreate, RestricaoAlimentarRead
from app.RestricaoAlimentar import service_restricao_alimentar

router = APIRouter(prefix="/restricao-alimentar", tags=["RestricaoAlimentar"])

@router.post("/", response_model=RestricaoAlimentarRead)
def create_restricao_alimentar(restricao: RestricaoAlimentarCreate, db: Session = Depends(get_db)):
    return service_restricao_alimentar.create_restricao_alimentar(db, restricao)

@router.get("/", response_model=List[RestricaoAlimentarRead])
def get_all_restricoes_alimentares(db: Session = Depends(get_db)):
    return service_restricao_alimentar.get_all_restricoes_alimentares(db)

@router.get("/{id}", response_model=RestricaoAlimentarRead)
def get_restricao_alimentar_by_id(id: int, db: Session = Depends(get_db)):
    restricao = service_restricao_alimentar.get_restricao_alimentar_by_id(db, id)
    if not restricao:
        raise HTTPException(status_code=404, detail="Restrição alimentar não encontrada")
    return restricao

@router.get("/nome/{nome}", response_model=RestricaoAlimentarRead)
def get_restricao_alimentar_by_nome(nome: str, db: Session = Depends(get_db)):
    restricao = service_restricao_alimentar.get_restricao_alimentar_by_nome(db, nome)
    if not restricao:
        raise HTTPException(status_code=404, detail="Restrição alimentar não encontrada")
    return restricao

@router.put("/{id}", response_model=RestricaoAlimentarRead)
def update_restricao_alimentar(id: int, restricao: RestricaoAlimentarCreate, db: Session = Depends(get_db)):
    return service_restricao_alimentar.update_restricao_alimentar(db, id, restricao)

@router.delete("/{id}")
def delete_restricao_alimentar(id: int, db: Session = Depends(get_db)):
    return service_restricao_alimentar.delete_restricao_alimentar(db, id)
