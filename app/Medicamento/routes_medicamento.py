from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.settings import get_db
from app.Medicamento.schema_medicamento import MedicamentoCreate, MedicamentoRead
from app.Medicamento import service_medicamento

router = APIRouter(prefix="/medicamento", tags=["Medicamento"])

@router.post("/", response_model=MedicamentoRead)
def create_medicamento(medicamento: MedicamentoCreate, db: Session = Depends(get_db)):
    return service_medicamento.create_medicamento(db, medicamento)

@router.get("/", response_model=List[MedicamentoRead])
def get_all_medicamentos(db: Session = Depends(get_db)):
    return service_medicamento.get_all_medicamentos(db)

@router.get("/{id}", response_model=MedicamentoRead)
def get_medicamento_by_id(id: int, db: Session = Depends(get_db)):
    medicamento = service_medicamento.get_medicamento_by_id(db, id)
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")
    return medicamento

# buscar a partir do nome
@router.get("/nome/{nome}", response_model=MedicamentoRead)
def get_medicamento_by_nome(nome: str, db: Session = Depends(get_db)):
    medicamento = service_medicamento.get_medicamento_by_nome(db, nome)
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")
    return medicamento

# buscar a partit do principio ativo
@router.get("/principio-ativo/{principio_ativo}", response_model=List[MedicamentoRead])
def get_medicamentos_by_principio_ativo(principio_ativo: str, db: Session = Depends(get_db)):
    medicamentos = service_medicamento.get_medicamentos_by_principio_ativo(db, principio_ativo)
    if not medicamentos:
        raise HTTPException(status_code=404, detail="Nenhum Medicamento encontrado para este princípio ativo")
    return medicamentos

# buscar a partir do fornecedor
@router.get("/fornecedor/{fornecedor_id}", response_model=List[MedicamentoRead])
def get_medicamentos_by_fornecedor(fornecedor_id: int, db: Session = Depends(get_db)):
    medicamentos = service_medicamento.get_medicamentos_by_fornecedor(db, fornecedor_id)
    if not medicamentos:
        raise HTTPException(status_code=404, detail="Nenhum Medicamento encontrado para este fornecedor")
    return medicamentos     

@router.put("/{id}", response_model=MedicamentoRead)
def update_medicamento(id: int, medicamento: MedicamentoCreate, db: Session = Depends(get_db)):
    updated_medicamento = service_medicamento.update_medicamento(db, id, medicamento)
    if not updated_medicamento:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")
    return updated_medicamento  

@router.delete("/{id}")
def delete_medicamento(id: int, db: Session = Depends(get_db)):
    deleted = service_medicamento.delete_medicamento(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")
    return {"detail": "Medicamento deletado com sucesso"}   

