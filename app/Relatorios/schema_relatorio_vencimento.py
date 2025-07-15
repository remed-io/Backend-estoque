from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from enum import Enum

class TipoVencimento(str, Enum):
    VENCIDO = "vencido"
    VENCE_HOJE = "vence_hoje"
    VENCE_AMANHA = "vence_amanha"
    VENCE_3_DIAS = "vence_3_dias"
    VENCE_7_DIAS = "vence_7_dias"
    VENCE_15_DIAS = "vence_15_dias"
    VENCE_30_DIAS = "vence_30_dias"

class StatusVencimento(str, Enum):
    VENCIDO = "vencido"
    CRITICO = "critico"  # Vence em até 3 dias
    ATENCAO = "atencao"  # Vence em até 15 dias
    NORMAL = "normal"    # Vence em mais de 15 dias

class ItemVencimento(BaseModel):
    item_estoque_id: int
    produto_id: int
    produto_nome: str
    tipo_produto: str
    codigo_barras: str
    lote: str
    data_validade: date
    dias_para_vencimento: int
    status_vencimento: StatusVencimento
    quantidade_atual: int
    valor_unitario: float
    valor_total: float
    fornecedor_id: int
    fornecedor_nome: str
    armazem_id: int
    armazem_nome: str

class ResumoVencimento(BaseModel):
    total_itens_analisados: int
    produtos_vencidos: int
    produtos_vence_hoje: int
    produtos_vence_amanha: int
    produtos_vence_3_dias: int
    produtos_vence_7_dias: int
    produtos_vence_15_dias: int
    produtos_vence_30_dias: int
    valor_total_vencidos: float
    valor_total_criticos: float
    valor_total_atencao: float

class RelatorioVencimento(BaseModel):
    data_geracao: date
    parametros: dict
    resumo: ResumoVencimento
    itens: List[ItemVencimento]
    
class FiltroRelatorioVencimento(BaseModel):
    dias_limite: int = Field(30, description="Dias limite para análise", ge=0, le=365)
    incluir_vencidos: bool = Field(True, description="Incluir produtos já vencidos")
    armazem_id: Optional[int] = Field(None, description="Filtrar por armazém específico")
    fornecedor_id: Optional[int] = Field(None, description="Filtrar por fornecedor específico")
    tipo_produto: Optional[str] = Field(None, description="Filtrar por tipo de produto")
    valor_minimo: Optional[float] = Field(None, description="Valor mínimo para incluir no relatório", ge=0)
    apenas_com_estoque: bool = Field(True, description="Incluir apenas itens com estoque > 0")

class ExportacaoConfig(BaseModel):
    formato: str = Field("json", description="Formato de exportação: json, csv, excel")
    incluir_resumo: bool = Field(True, description="Incluir resumo no arquivo")
    agrupar_por_produto: bool = Field(False, description="Agrupar itens pelo mesmo produto")
