from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.settings import get_db
from app.security import get_current_user
from app.Funcionario.model_funcionario import Funcionario
from app.Relatorios.schema_relatorio_vencimento import (
    RelatorioVencimento,
    FiltroRelatorioVencimento,
    ItemVencimento,
    ExportacaoConfig
)
from app.Relatorios import service_relatorio_vencimento
import io
from datetime import date

router = APIRouter(prefix="/relatorios/vencimento", tags=["Relatórios - Vencimento"])

@router.get("/", response_model=RelatorioVencimento)
def gerar_relatorio_vencimento(
    dias_limite: int = Query(30, description="Dias limite para análise", ge=0, le=365),
    incluir_vencidos: bool = Query(True, description="Incluir produtos já vencidos"),
    armazem_id: int = Query(None, description="Filtrar por armazém específico"),
    fornecedor_id: int = Query(None, description="Filtrar por fornecedor específico"),
    tipo_produto: str = Query(None, description="Filtrar por tipo de produto"),
    valor_minimo: float = Query(None, description="Valor mínimo para incluir", ge=0),
    apenas_com_estoque: bool = Query(True, description="Apenas itens com estoque > 0"),
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """Gerar relatório completo de produtos vencidos e próximos do vencimento"""
    
    filtros = FiltroRelatorioVencimento(
        dias_limite=dias_limite,
        incluir_vencidos=incluir_vencidos,
        armazem_id=armazem_id,
        fornecedor_id=fornecedor_id,
        tipo_produto=tipo_produto,
        valor_minimo=valor_minimo,
        apenas_com_estoque=apenas_com_estoque
    )
    
    return service_relatorio_vencimento.gerar_relatorio_vencimento(db, filtros)

@router.get("/csv")
def exportar_relatorio_csv(
    dias_limite: int = Query(30, description="Dias limite para análise", ge=0, le=365),
    incluir_vencidos: bool = Query(True, description="Incluir produtos já vencidos"),
    armazem_id: int = Query(None, description="Filtrar por armazém específico"),
    fornecedor_id: int = Query(None, description="Filtrar por fornecedor específico"),
    tipo_produto: str = Query(None, description="Filtrar por tipo de produto"),
    valor_minimo: float = Query(None, description="Valor mínimo para incluir", ge=0),
    apenas_com_estoque: bool = Query(True, description="Apenas itens com estoque > 0"),
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """Exportar relatório de vencimento em formato CSV"""
    
    filtros = FiltroRelatorioVencimento(
        dias_limite=dias_limite,
        incluir_vencidos=incluir_vencidos,
        armazem_id=armazem_id,
        fornecedor_id=fornecedor_id,
        tipo_produto=tipo_produto,
        valor_minimo=valor_minimo,
        apenas_com_estoque=apenas_com_estoque
    )
    
    relatorio = service_relatorio_vencimento.gerar_relatorio_vencimento(db, filtros)
    csv_content = service_relatorio_vencimento.exportar_relatorio_csv(relatorio)
    
    # Nome do arquivo com data
    hoje = date.today().strftime("%Y%m%d")
    filename = f"relatorio_vencimento_{hoje}.csv"
    
    # Retornar como download
    return StreamingResponse(
        io.StringIO(csv_content),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/vencidos-hoje", response_model=List[ItemVencimento])
def produtos_vencidos_hoje(
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """Produtos que vencem hoje - para dashboard/alertas"""
    return service_relatorio_vencimento.obter_produtos_vencidos_hoje(db)

@router.get("/criticos", response_model=List[ItemVencimento])
def produtos_criticos(
    dias_limite: int = Query(3, description="Dias limite para considerar crítico", ge=0, le=7),
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """Produtos em situação crítica (vencimento muito próximo)"""
    return service_relatorio_vencimento.obter_produtos_criticos(db, dias_limite)

@router.get("/resumo-rapido")
def resumo_vencimento_rapido(
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """Resumo rápido para dashboard - produtos críticos dos próximos 7 dias"""
    
    filtros = FiltroRelatorioVencimento(
        dias_limite=7,
        incluir_vencidos=True,
        apenas_com_estoque=True
    )
    
    relatorio = service_relatorio_vencimento.gerar_relatorio_vencimento(db, filtros)
    
    return {
        "data_consulta": date.today(),
        "produtos_vencidos": relatorio.resumo.produtos_vencidos,
        "vence_hoje": relatorio.resumo.produtos_vence_hoje,
        "vence_amanha": relatorio.resumo.produtos_vence_amanha,
        "vence_3_dias": relatorio.resumo.produtos_vence_3_dias,
        "vence_7_dias": relatorio.resumo.produtos_vence_7_dias,
        "valor_comprometido": relatorio.resumo.valor_total_vencidos + relatorio.resumo.valor_total_criticos
    }

@router.get("/por-armazem/{armazem_id}", response_model=RelatorioVencimento)
def relatorio_vencimento_por_armazem(
    armazem_id: int,
    dias_limite: int = Query(30, description="Dias limite para análise", ge=0, le=365),
    incluir_vencidos: bool = Query(True, description="Incluir produtos já vencidos"),
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """Relatório de vencimento específico de um armazém"""
    
    filtros = FiltroRelatorioVencimento(
        dias_limite=dias_limite,
        incluir_vencidos=incluir_vencidos,
        armazem_id=armazem_id,
        apenas_com_estoque=True
    )
    
    return service_relatorio_vencimento.gerar_relatorio_vencimento(db, filtros)

@router.get("/por-fornecedor/{fornecedor_id}", response_model=RelatorioVencimento)
def relatorio_vencimento_por_fornecedor(
    fornecedor_id: int,
    dias_limite: int = Query(30, description="Dias limite para análise", ge=0, le=365),
    incluir_vencidos: bool = Query(True, description="Incluir produtos já vencidos"),
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """Relatório de vencimento específico de um fornecedor"""
    
    filtros = FiltroRelatorioVencimento(
        dias_limite=dias_limite,
        incluir_vencidos=incluir_vencidos,
        fornecedor_id=fornecedor_id,
        apenas_com_estoque=True
    )
    
    return service_relatorio_vencimento.gerar_relatorio_vencimento(db, filtros)
