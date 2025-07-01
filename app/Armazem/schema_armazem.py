#app/schema/armazem_schema.py
from pydantic import BaseModel
from typing import Optional

class ArmazemBase(BaseModel):
    local_armazem: str

class ArmazemCreate(ArmazemBase):
    pass

class ArmazemRead(ArmazemBase):
    id: int

    class Config:
        from_attributes = True