from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime

class MovimentacaoEstoqueBase(BaseModel):
    data_movimentacao: datetime
    tipo: str
    quantidade: int
    item_estoque_id: int
    funcionario_id: int
    cpf_comprador: Optional[str] = None
    nome_comprador: Optional[str] = None
    receita_digital: Optional[str] = None
    armazem_id: int

class MovimentacaoEstoqueCreate(MovimentacaoEstoqueBase):
    pass

class MovimentacaoEstoqueRead(MovimentacaoEstoqueBase):
    id: int

    class Config:
        orm_mode = True
