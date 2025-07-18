from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum  # TarjaEnum removed to allow free-text tarja values

class MedicamentoBase(BaseModel):
    nome: str = Field(..., max_length=100)
    descricao: Optional[str] = Field(None, max_length=255)
    dosagem: Optional[str] = Field(None, max_length=50)
    principio_ativo: Optional[str] = Field(None, max_length=100)
    tarja: Optional[str] = Field(None, max_length=50)
    necessita_receita: Optional[bool] = False
    forma_farmaceutica: Optional[str] = Field(None, max_length=50)
    fabricante: Optional[str] = Field(None, max_length=100)
    registro_anvisa: Optional[str] = Field(None, max_length=50)

class MedicamentoCreate(MedicamentoBase):
    pass

class MedicamentoRead(MedicamentoBase):
    id: int

    class Config:
        from_attributes = True