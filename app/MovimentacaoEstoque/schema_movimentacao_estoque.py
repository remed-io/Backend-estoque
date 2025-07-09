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

    @model_validator(mode='after')
    def check_saida_fields(cls, values):
        tipo = values.tipo
        if tipo and tipo.lower() == 'saida':
            if not values.cpf_comprador or not values.nome_comprador or not values.receita_digital:
                raise ValueError('cpf_comprador, nome_comprador e receita_digital são obrigatórios para movimentações do tipo "saida"')
        return values

class MovimentacaoEstoqueCreate(MovimentacaoEstoqueBase):
    pass

class MovimentacaoEstoqueRead(MovimentacaoEstoqueBase):
    id: int

    class Config:
        orm_mode = True
