#app/schema/subcategoria_cuidado_pessoal_schema.py

from pydantic import BaseModel, Field
from typing import Optional

class SubcategoriaCuidadoPessoalBase(BaseModel):
    nome: str = Field(..., max_length=100)
    descricao: Optional[str] = Field(None, max_length=255)

class SubcategoriaCuidadoPessoalCreate(SubcategoriaCuidadoPessoalBase):
    pass

class SubcategoriaCuidadoPessoalRead(SubcategoriaCuidadoPessoalBase):
    id: int

    class Config:
        orm_mode = True