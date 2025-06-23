from pydantic import BaseModel
from datetime import datetime

class ItemEstoqueBase(BaseModel):
    codigo_barras: str
    produto_nome: str
    preco: float
    validade: datetime
    fornecedor_id: int

class ItemEstoqueCreate(ItemEstoqueBase):
    pass

class ItemEstoqueRead(ItemEstoqueBase):
    id: int

    class Config:
        orm_mode = True
