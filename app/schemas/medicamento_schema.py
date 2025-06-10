# app/schemas/medicamento_schema

from pydantic import BaseModel, Field
from typing import Optional

class MedicamentoBase(BaseModel):
    nome: str = Field(..., max_length=100)
    descricao: Optional[str] = Field(None, max_length=255)
    principio_ativo: Optional[str] = Field(None, max_length=100)
    tarja: Optional[str] = Field(None, max_length=50)
    restricoes: Optional[str] = None
    fabricante: Optional[str] = Field(None, max_length=100)
    registro_anvisa: Optional[str] = Field(None, max_length=50)

class MedicamentoCreate(MedicamentoBase):
    pass

class MedicamentoRead(MedicamentoBase):
    id: int

    class Config:
        orm_mode = True