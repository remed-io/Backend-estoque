from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class TipoMovimentacao(str, Enum):
    entrada = "entrada"
    saida = "saida"

class FiltroRelatorioMovimentacao(BaseModel):
    """Schema para filtros do relatório de movimentações"""
    data_inicio: Optional[date] = Field(None, description="Data inicial do período")
    data_fim: Optional[date] = Field(None, description="Data final do período")
    tipo: Optional[TipoMovimentacao] = Field(None, description="Tipo de movimentação (entrada/saida)")
    produto_nome: Optional[str] = Field(None, description="Nome do produto para filtrar")
    armazem_id: Optional[int] = Field(None, description="ID do armazém")
    funcionario_id: Optional[int] = Field(None, description="ID do funcionário responsável")
    item_id: Optional[int] = Field(None, description="ID do item de estoque")
    
class MovimentacaoResumo(BaseModel):
    """Schema para dados resumidos de uma movimentação"""
    id: int
    data: datetime
    tipo: str
    quantidade: int
    
    # Dados do item
    item_id: int
    produto_nome: str
    lote: str
    data_vencimento: date
    preco_custo: float
    
    # Dados do armazém
    armazem_id: int
    armazem_nome: str
    
    # Dados do funcionário
    funcionario_id: int
    funcionario_nome: str
    
    # Dados específicos para saída (podem ser nulos)
    cpf_comprador: Optional[str] = None
    nome_comprador: Optional[str] = None
    receita_digital: Optional[str] = None

class EstatisticasMovimentacao(BaseModel):
    """Schema para estatísticas das movimentações"""
    total_movimentacoes: int
    total_entradas: int
    total_saidas: int
    quantidade_total_entrada: int
    quantidade_total_saida: int
    valor_total_entrada: float
    valor_total_saida: float
    periodo_inicio: Optional[date] = None
    periodo_fim: Optional[date] = None

class RelatorioMovimentacao(BaseModel):
    """Schema principal do relatório de movimentações"""
    movimentacoes: List[MovimentacaoResumo]
    estatisticas: EstatisticasMovimentacao
    filtros_aplicados: FiltroRelatorioMovimentacao

class ExportConfig(BaseModel):
    """Configurações para exportação do relatório"""
    formato: str = Field(default="json", description="Formato de exportação (json/csv)")
    incluir_estatisticas: bool = Field(default=True, description="Incluir estatísticas no export")

class ItemMaisVendidoResponse(BaseModel):
    """Resposta com o item mais vendido/retirado no período"""
    item: str
