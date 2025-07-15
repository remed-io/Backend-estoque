from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class StatusEstoque(str, Enum):
    VENCIDO = "vencido"
    PROXIMO_VENCIMENTO = "proximo_vencimento"
    ESTOQUE_BAIXO = "estoque_baixo"
    ESTOQUE_CRITICO = "estoque_critico"
    NORMAL = "normal"

class TipoProduto(str, Enum):
    MEDICAMENTO = "medicamento"
    CUIDADO_PESSOAL = "cuidado_pessoal"
    SUPLEMENTO_ALIMENTAR = "suplemento_alimentar"

class ConsultaEstoqueBase(BaseModel):
    item_estoque_id: int
    produto_id: int
    produto_nome: str
    tipo_produto: TipoProduto
    codigo_barras: str
    preco: float
    data_validade: date
    lote: str
    fornecedor_id: int
    fornecedor_nome: str
    armazem_id: int
    armazem_local: str
    quantidade_atual: int
    quantidade_minima: int
    status: StatusEstoque
    dias_para_vencimento: Optional[int] = None

class ConsultaEstoqueRead(ConsultaEstoqueBase):
    pass

class FiltroConsultaEstoque(BaseModel):
    # Filtros de produto
    produto_nome: Optional[str] = Field(None, description="Filtrar por nome do produto (busca parcial)")
    codigo_barras: Optional[str] = Field(None, description="Filtrar por código de barras")
    tipo_produto: Optional[TipoProduto] = Field(None, description="Filtrar por tipo de produto")
    
    # Filtros de fornecedor e armazém
    fornecedor_id: Optional[int] = Field(None, description="Filtrar por fornecedor")
    armazem_id: Optional[int] = Field(None, description="Filtrar por armazém")
    
    # Filtros de validade
    vencidos: Optional[bool] = Field(None, description="Mostrar apenas produtos vencidos")
    dias_vencimento: Optional[int] = Field(None, description="Produtos que vencem em X dias", ge=0)
    
    # Filtros de estoque
    estoque_baixo: Optional[bool] = Field(None, description="Mostrar apenas itens com estoque baixo")
    estoque_critico: Optional[bool] = Field(None, description="Mostrar apenas itens com estoque crítico")
    quantidade_min: Optional[int] = Field(None, description="Filtrar por quantidade mínima", ge=0)
    quantidade_max: Optional[int] = Field(None, description="Filtrar por quantidade máxima", ge=0)
    
    # Filtros de status
    status: Optional[List[StatusEstoque]] = Field(None, description="Filtrar por status específicos")

class ResumoEstoque(BaseModel):
    total_itens: int
    total_produtos_diferentes: int
    produtos_vencidos: int
    produtos_proximo_vencimento: int
    produtos_estoque_baixo: int
    produtos_estoque_critico: int
    valor_total_estoque: float

class EstoqueDetalhado(BaseModel):
    resumo: ResumoEstoque
    itens: List[ConsultaEstoqueRead]
