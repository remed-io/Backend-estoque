from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from enum import Enum

class TipoAlerta(str, Enum):
    estoque_critico = "estoque_critico"
    estoque_zero = "estoque_zero"
    produto_vencido = "produto_vencido"
    produto_proximo_vencimento = "produto_proximo_vencimento"

class SeveridadeAlerta(str, Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"
    critica = "critica"

class AlertaEstoque(BaseModel):
    """Schema para alerta individual de estoque"""
    id: str = Field(description="ID único do alerta")
    tipo: TipoAlerta = Field(description="Tipo do alerta")
    severidade: SeveridadeAlerta = Field(description="Severidade do alerta")
    titulo: str = Field(description="Título do alerta")
    descricao: str = Field(description="Descrição detalhada do alerta")
    data_alerta: date = Field(description="Data do alerta")
    
    # Dados do produto/item
    produto_nome: str = Field(description="Nome do produto")
    categoria: str = Field(description="Categoria do produto")
    
    # Dados do estoque
    armazem_id: int = Field(description="ID do armazém")
    armazem_nome: str = Field(description="Nome do armazém")
    quantidade_atual: int = Field(description="Quantidade atual em estoque")
    quantidade_minima: int = Field(description="Quantidade mínima configurada")
    
    # Dados específicos para itens com vencimento
    item_id: Optional[int] = Field(None, description="ID do item de estoque específico")
    lote: Optional[str] = Field(None, description="Lote do produto")
    data_vencimento: Optional[date] = Field(None, description="Data de vencimento")
    dias_para_vencer: Optional[int] = Field(None, description="Dias até o vencimento")

class FiltroAlertas(BaseModel):
    """Schema para filtros de alertas"""
    tipos: Optional[List[TipoAlerta]] = Field(None, description="Tipos de alerta a filtrar")
    severidades: Optional[List[SeveridadeAlerta]] = Field(None, description="Severidades a filtrar")
    armazem_id: Optional[int] = Field(None, description="ID do armazém")
    produto_nome: Optional[str] = Field(None, description="Nome do produto")
    apenas_criticos: bool = Field(False, description="Apenas alertas críticos e altos")

class ResumoAlertas(BaseModel):
    """Schema para resumo dos alertas"""
    total_alertas: int = Field(description="Total de alertas ativos")
    alertas_criticos: int = Field(description="Alertas críticos")
    alertas_altos: int = Field(description="Alertas de severidade alta")
    alertas_medios: int = Field(description="Alertas de severidade média")
    alertas_baixos: int = Field(description="Alertas de severidade baixa")
    
    # Por tipo
    estoque_critico: int = Field(description="Alertas de estoque crítico")
    estoque_zero: int = Field(description="Alertas de estoque zerado")
    produtos_vencidos: int = Field(description="Produtos vencidos")
    produtos_proximo_vencimento: int = Field(description="Produtos próximos ao vencimento")
    
    # Por armazém
    armazens_afetados: int = Field(description="Número de armazéns com alertas")

class ConfiguracaoAlertas(BaseModel):
    """Schema para configuração dos alertas"""
    dias_aviso_vencimento: int = Field(
        default=30,
        description="Dias antes do vencimento para emitir alerta"
    )
    incluir_vencidos: bool = Field(
        default=True,
        description="Incluir produtos já vencidos nos alertas"
    )
    incluir_estoque_zero: bool = Field(
        default=True,
        description="Incluir alertas de estoque zerado"
    )
    severidade_estoque_critico: SeveridadeAlerta = Field(
        default=SeveridadeAlerta.alta,
        description="Severidade para estoque crítico"
    )
    severidade_estoque_zero: SeveridadeAlerta = Field(
        default=SeveridadeAlerta.critica,
        description="Severidade para estoque zerado"
    )

class RelatorioAlertas(BaseModel):
    """Schema principal do relatório de alertas"""
    alertas: List[AlertaEstoque] = Field(description="Lista de alertas")
    resumo: ResumoAlertas = Field(description="Resumo dos alertas")
    configuracao: ConfiguracaoAlertas = Field(description="Configuração utilizada")
    data_geracao: date = Field(description="Data de geração do relatório")
