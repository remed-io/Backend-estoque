#app/schema/restricao_schema.py
from pydantic import BaseModel

class RestricaoAlimentarBase(BaseModel):
    nome: str

class RestricaoAlimentarCreate(RestricaoAlimentarBase):
    pass

class RestricaoAlimentarRead(RestricaoAlimentarBase):
    id: int

    class Config:
        orm_mode = True
