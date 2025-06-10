# app/schema/cuidado_pessoal_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CuidadoPessoalBase(BaseModel):
    nome: str = Field(..., max_length=100)
    descricao: Optional[str] = Field(None, max_length=255)
    subcategoria_id: Optional[int] = None
    forma: Optional[str] = Field(None, max_length=50)
    quantidade: Optional[str] = Field(None, max_length=20)
    volume: Optional[str] = Field(None, max_length=20)
    uso_recomendado: Optional[str] = Field(None, max_length=100)
    publico_alvo: Optional[str] = Field(None, max_length=50)
    fabricante: Optional[str] = Field(None, max_length=100)

class CuidadoPessoalCreate(CuidadoPessoalBase):
    pass

class CuidadoPessoalRead(CuidadoPessoalBase):
    id: int

    class Config:
        orm_mode = True

class CuidadoPessoalWithSubcategoria(CuidadoPessoalRead):
    subcategoria_nome: Optional[str]
    subcategoria_descricao: Optional[str]