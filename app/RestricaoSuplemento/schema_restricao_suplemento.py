from pydantic import BaseModel
from typing import Optional

class RestricaoSuplementoBase(BaseModel):
    suplemento_alimentar_id: int
    restricao_alimentar_id: int
    severidade: Optional[str]
    observacoes: Optional[str]

class RestricaoSuplementoCreate(RestricaoSuplementoBase):
    pass

class RestricaoSuplementoRead(RestricaoSuplementoBase):
    class Config:
        orm_mode = True 