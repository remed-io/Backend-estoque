from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemArmazenadoBase(BaseModel):
    armazem_id: int
    item_estoque_id: int
    quantidade: int

class ItemArmazenadoCreate(ItemArmazenadoBase):
    pass

class ItemArmazenadoRead(ItemArmazenadoBase):
    id: int
    data_atualizacao: datetime

    class Config:
        orm_mode = True 