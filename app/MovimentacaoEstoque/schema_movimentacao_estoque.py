from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MovimentacaoEstoqueBase(BaseModel):
    data: datetime
    tipo: str
    quantidade: int
    item_id: int
    responsavel_id: int
    cpf_comprador: Optional[str] = None
    nome_comprador: Optional[str] = None
    receita_digital: Optional[str] = None

class MovimentacaoEstoqueCreate(MovimentacaoEstoqueBase):
    pass

class MovimentacaoEstoqueRead(MovimentacaoEstoqueBase):
    id: int

    class Config:
        orm_mode = True
