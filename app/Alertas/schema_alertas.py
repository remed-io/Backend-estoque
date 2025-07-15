from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class TipoAlerta(str, Enum):
    ESTOQUE_CRITICO = "estoque_critico"
    ESTOQUE_BAIXO = "estoque_baixo"
    PRODUTO_VENCIDO = "produto_vencido"
    PROXIMO_VENCIMENTO = "proximo_vencimento"
    FALTA_PRODUTO = "falta_produto"

class PrioridadeAlerta(str, Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"

class AlertaEstoque(BaseModel):
    """Schema para um alerta de estoque individual"""
    id: Optional[int] = None
    tipo: TipoAlerta
    prioridade: PrioridadeAlerta
    titulo: str = Field(..., description="Título do alerta")
    descricao: str = Field(..., description="Descrição detalhada do problema")
    item_estoque_id: int
    produto_nome: str
    codigo_barras: str
    armazem_id: int
    armazem_nome: str
    quantidade_atual: int
    quantidade_minima: int
    data_validade: Optional[datetime] = None
    dias_para_vencimento: Optional[int] = None
    valor_unitario: float
    valor_total_impactado: float
    data_criacao: datetime = Field(default_factory=datetime.now)
    data_resolucao: Optional[datetime] = None
    resolvido: bool = False
    observacoes: Optional[str] = None

    class Config:
        from_attributes = True

class AlertaCritico(BaseModel):
    """Schema simplificado para alertas críticos urgentes"""
    tipo: TipoAlerta
    prioridade: PrioridadeAlerta
    produto_nome: str
    armazem_nome: str
    quantidade_atual: int
    quantidade_minima: int
    valor_impacto: float
    urgencia_dias: Optional[int] = None  # Para vencimento

class ResumoAlertas(BaseModel):
    """Resumo geral dos alertas do sistema"""
    total_alertas: int
    alertas_criticos: int
    alertas_altos: int
    alertas_medios: int
    alertas_baixos: int
    produtos_em_falta: int
    produtos_vencidos: int
    produtos_vencendo_hoje: int
    produtos_vencendo_3_dias: int
    valor_total_impactado: float
    ultima_atualizacao: datetime

class FiltroAlertas(BaseModel):
    """Filtros para consulta de alertas"""
    tipo: Optional[TipoAlerta] = None
    prioridade: Optional[PrioridadeAlerta] = None
    armazem_id: Optional[int] = None
    apenas_nao_resolvidos: bool = True
    dias_vencimento_max: Optional[int] = None

class RelatorioAlertas(BaseModel):
    """Relatório completo de alertas"""
    resumo: ResumoAlertas
    alertas_criticos: List[AlertaCritico]
    alertas_completos: List[AlertaEstoque]
    filtros_aplicados: FiltroAlertas
    data_geracao: datetime = Field(default_factory=datetime.now)

class ConfiguracaoAlertas(BaseModel):
    """Configurações do sistema de alertas"""
    dias_vencimento_critico: int = Field(default=3, description="Dias para alerta crítico de vencimento")
    dias_vencimento_atencao: int = Field(default=7, description="Dias para alerta de atenção")
    dias_vencimento_aviso: int = Field(default=30, description="Dias para aviso de vencimento")
    ativar_alertas_email: bool = Field(default=False, description="Enviar alertas por email")
    ativar_alertas_push: bool = Field(default=True, description="Exibir alertas no sistema")
    
class NotificacaoAlerta(BaseModel):
    """Schema para notificações de alerta"""
    id: Optional[int] = None
    alerta_id: int
    funcionario_id: Optional[int] = None
    tipo_notificacao: str = Field(..., description="email, push, sms")
    enviado: bool = False
    data_envio: Optional[datetime] = None
    tentativas_envio: int = 0
    erro_envio: Optional[str] = None
    
    class Config:
        from_attributes = True
