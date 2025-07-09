#app/schema/armazem_schema.py
from pydantic import BaseModel, Field
from typing import Optional

class ArmazemBase(BaseModel):
    local_armazem: str
    quantidade_minima: int = Field(default=0, ge=0, description="Quantidade mínima para alertas de estoque")

class ArmazemCreate(ArmazemBase):
    pass

class ArmazemRead(ArmazemBase):
    id: int

    class Config:
        from_attributes = True