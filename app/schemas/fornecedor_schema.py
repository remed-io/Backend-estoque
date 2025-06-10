#app/schema/fornecedor_schema.py
from pydantic import BaseModel
from typing import Optional

class FornecedorBase(BaseModel):
    nome: str
    cnpj: str
    contato: Optional[str] = None

class FornecedorCreate(FornecedorBase):
    pass

class FornecedorRead(FornecedorBase):
    id: int

    class Config:
        orm_mode = True