from pydantic import BaseModel, root_validator
from typing import Optional
from datetime import datetime

class ItemEstoqueBase(BaseModel):
    codigo_barras: str
    produto_nome: str
    preco: float
    validade: datetime
    fornecedor_id: int

class ItemEstoqueCreate(ItemEstoqueBase):
    produto_medicamento_id: Optional[int] = None
    produto_cuidado_pessoal_id: Optional[int] = None
    produto_suplemento_alimentar_id: Optional[int] = None
    
    @root_validator
    def validar_cadastro_produto(cls, values):
        tipo_produto = [
            values.get('produto_medicamento_id'),
            values.get('produto_cuidado_pessoal_id'),
            values.get('produto_suplemento_alimentar_id')
        ]
        preenchidos = sum(1 for v in tipo_produto if v is not None)
        if preenchidos != 1:
            raise ValueError(
                "Deve ser preenchido apenas um tipo de produto:"
                "medicamento, cuidado pessoal ou suplemento alimentar."
            )
        return values

class ItemEstoqueRead(ItemEstoqueBase):
    id: int

    class Config:
        orm_mode = True
