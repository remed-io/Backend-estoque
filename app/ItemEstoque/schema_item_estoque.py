from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime

class ItemEstoqueBase(BaseModel):
    codigo_barras: str
    preco: float
    data_validade: datetime
    fornecedor_id: int
    produto_id: Optional[int] = None
    produto_nome: Optional[str] = None
    tipo_produto: Optional[str] = None

class ItemEstoqueCreate(ItemEstoqueBase):
    medicamento_id: Optional[int] = None
    cuidado_pessoal_id: Optional[int] = None
    suplemento_alimentar_id: Optional[int] = None

    @model_validator(mode='after')
    def validar_cadastro_produto(cls, values):
        tipo_produto = [
            values.medicamento_id,
            values.cuidado_pessoal_id,
            values.suplemento_alimentar_id
        ]
        preenchidos = sum(1 for v in tipo_produto if v is not None)
        if preenchidos != 1:
            raise ValueError(
                "Deve ser preenchido apenas um tipo de produto: "
                "medicamento, cuidado pessoal ou suplemento alimentar."
            )
        return values

class ItemEstoqueRead(ItemEstoqueBase):
    id: int

    class Config:
        orm_mode = True
