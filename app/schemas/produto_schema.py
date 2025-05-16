from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str
    preco: float
    validade: Optional[datetime]

class ProdutoCreate(ProdutoBase):
    pass 

class ProdutoOut(ProdutoBase):
    id: int

    class Config:
        from_attributes = True 
