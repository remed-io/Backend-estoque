#app/schema/armazenamento_schema.py
from pydantic import BaseModel
from typing import Optional

class ArmazenamentoBase(BaseModel):
    local_armazenamento: str

class ArmazenamentoCreate(ArmazenamentoBase):
    pass

class ArmazenamentoRead(ArmazenamentoBase):
    id: int

    class Config:
        orm_mode = True