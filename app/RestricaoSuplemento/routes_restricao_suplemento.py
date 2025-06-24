from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.settings import get_db
from app.RestricaoSuplemento.schema_restricao_suplemento import RestricaoSuplementoCreate, RestricaoSuplementoRead
from app.RestricaoSuplemento.service_restricao_suplemento import criar_restricao_suplemento, listar_restricoes_suplemento
from typing import List

router = APIRouter(prefix="/restricao_suplemento", tags=["RestricaoSuplemento"])
       
@router.post("/", response_model=RestricaoSuplementoRead)
def criar(item: RestricaoSuplementoCreate, db: Session = Depends(get_db)):
    return criar_restricao_suplemento(db, item)

@router.get("/", response_model=List[RestricaoSuplementoRead])
def listar(db: Session = Depends(get_db)):
    return listar_restricoes_suplemento(db)

 