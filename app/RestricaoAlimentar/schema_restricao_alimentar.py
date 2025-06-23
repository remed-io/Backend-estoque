#app/schema/restricao_schema.py
from pydantic import BaseModel

class RestricaoBase(BaseModel):
    nome: str

class RestricaoCreate(RestricaoBase):
    pass

class RestricaoRead(RestricaoBase):
    id: int

    class Config:
        orm_mode = True
