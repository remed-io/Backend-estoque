from pydantic import BaseModel, Field
from typing import Optional

class SuplementoAlimentarBase(BaseModel):
    nome: str = Field(..., max_length=100)
    descricao: Optional[str] = Field(None, max_length=255)
    principio_ativo: Optional[str] = Field(None, max_length=100)
    sabor: Optional[str] = Field(None, max_length=50)
    peso_volume: Optional[str] = Field(None, max_length=20)
    fabricante: Optional[str] = Field(None, max_length=100)
    registro_anvisa: Optional[str] = Field(None, max_length=50)

class SuplementoAlimentarCreate(SuplementoAlimentarBase):
    pass

class SuplementoAlimentarRead(SuplementoAlimentarBase):
    id: int

    class Config:
        orm_mode = True