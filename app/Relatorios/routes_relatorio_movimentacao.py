from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date, datetime
import io

from app.settings import get_db



from .schema_relatorio_movimentacao import (
    FiltroRelatorioMovimentacao,
    RelatorioMovimentacao,
    EstatisticasMovimentacao,
    TipoMovimentacao,
    ExportConfig,
    ItemMaisVendidoResponse
)
from .service_relatorio_movimentacao import ServiceRelatorioMovimentacao

router = APIRouter(
    prefix="/relatorios/movimentacoes",
    tags=["Relatórios - Movimentações"]
)

@router.get("/mais-vendido", response_model=ItemMaisVendidoResponse)
def obter_item_mais_vendido(
    mes: int = Query(..., ge=1, le=12, description="Mês para relatório"),
    ano: int = Query(..., description="Ano para relatório"),
    db: Session = Depends(get_db),
):
    """
    Retorna o item mais retirado (mais vendido) no mês/ano especificado.
    """
    try:
        from calendar import monthrange
        inicio = date(ano, mes, 1)
        fim = date(ano, mes, monthrange(ano, mes)[1])
        item = ServiceRelatorioMovimentacao.obter_item_mais_vendido(db, inicio, fim)
        return ItemMaisVendidoResponse(item=item or "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter item mais vendido: {e}")

@router.get("/", response_model=RelatorioMovimentacao)
def obter_relatorio_movimentacoes(
    data_inicio: Optional[date] = Query(None, description="Data inicial do período (YYYY-MM-DD)"),
    data_fim: Optional[date] = Query(None, description="Data final do período (YYYY-MM-DD)"),
    tipo: Optional[TipoMovimentacao] = Query(None, description="Tipo de movimentação"),
    produto_nome: Optional[str] = Query(None, description="Nome do produto para filtrar"),
    armazem_id: Optional[int] = Query(None, description="ID do armazém"),
    funcionario_id: Optional[int] = Query(None, description="ID do funcionário responsável"),
    item_id: Optional[int] = Query(None, description="ID do item de estoque"),
    db: Session = Depends(get_db),
):
    """
    Gera relatório completo de movimentações de estoque com filtros opcionais.
    
    **Filtros disponíveis:**
    - **data_inicio/data_fim**: Período das movimentações
    - **tipo**: Tipo de movimentação (entrada/saida)
    - **produto_nome**: Nome do produto (busca parcial)
    - **armazem_id**: ID do armazém específico
    - **funcionario_id**: ID do funcionário responsável
    - **item_id**: ID do item de estoque específico
    
    **Retorna:**
    - Lista de movimentações com detalhes completos
    - Estatísticas consolidadas do período
    - Filtros aplicados
    """
    try:
        filtros = FiltroRelatorioMovimentacao(
            data_inicio=data_inicio,
            data_fim=data_fim,
            tipo=tipo,
            produto_nome=produto_nome,
            armazem_id=armazem_id,
            funcionario_id=funcionario_id,
            item_id=item_id
        )
        
        relatorio = ServiceRelatorioMovimentacao.gerar_relatorio(db, filtros)
        return relatorio
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar relatório de movimentações: {str(e)}"
        )

@router.get("/estatisticas", response_model=EstatisticasMovimentacao)
def obter_estatisticas_movimentacoes(
    data_inicio: Optional[date] = Query(None, description="Data inicial do período (YYYY-MM-DD)"),
    data_fim: Optional[date] = Query(None, description="Data final do período (YYYY-MM-DD)"),
    mes: Optional[int] = Query(None, ge=1, le=12, description="Mês para relatório rápido"),
    ano: Optional[int] = Query(None, description="Ano para relatório rápido"),
    db: Session = Depends(get_db),
):
    """
    Obtém apenas as estatísticas das movimentações para um período.
    
    **Útil para dashboards e visões gerais rápidas.**
    
    **Retorna:**
    - Total de movimentações
    - Quantidades de entrada e saída
    - Valores totais movimentados
    """
    try:
        # Se mês e ano informados, define início e fim do mês
        if mes and ano:
            from calendar import monthrange
            inicio = date(ano, mes, 1)
            fim = date(ano, mes, monthrange(ano, mes)[1])
            data_inicio, data_fim = inicio, fim
        estatisticas = ServiceRelatorioMovimentacao.obter_resumo_periodo(
            db, data_inicio, data_fim
        )
        return estatisticas
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter estatísticas: {str(e)}"
        )

@router.get("/estatisticas/mes-atual", response_model=EstatisticasMovimentacao)
def obter_estatisticas_mes_atual(
    db: Session = Depends(get_db),
):
    """
    Obtém estatísticas das movimentações apenas do mês atual.
    
    **Específico para Dashboard - mostra receita do mês.**
    """
    try:
        from datetime import date
        hoje = date.today()
        inicio_mes = date(hoje.year, hoje.month, 1)
        
        estatisticas = ServiceRelatorioMovimentacao.obter_resumo_periodo(
            db, inicio_mes, hoje
        )
        return estatisticas
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter estatísticas do mês: {str(e)}"
        )

@router.get("/export/csv")
def exportar_movimentacoes_csv(
    data_inicio: Optional[date] = Query(None, description="Data inicial do período"),
    data_fim: Optional[date] = Query(None, description="Data final do período"),
    tipo: Optional[TipoMovimentacao] = Query(None, description="Tipo de movimentação"),
    produto_nome: Optional[str] = Query(None, description="Nome do produto para filtrar"),
    armazem_id: Optional[int] = Query(None, description="ID do armazém"),
    funcionario_id: Optional[int] = Query(None, description="ID do funcionário responsável"),
    item_id: Optional[int] = Query(None, description="ID do item de estoque"),
    db: Session = Depends(get_db),
):
    """
    Exporta relatório de movimentações em formato CSV.
    
    **Inclui:**
    - Todas as movimentações com detalhes
    - Estatísticas consolidadas
    - Formatação adequada para Excel/LibreOffice
    """
    try:
        filtros = FiltroRelatorioMovimentacao(
            data_inicio=data_inicio,
            data_fim=data_fim,
            tipo=tipo,
            produto_nome=produto_nome,
            armazem_id=armazem_id,
            funcionario_id=funcionario_id,
            item_id=item_id
        )
        
        relatorio = ServiceRelatorioMovimentacao.gerar_relatorio(db, filtros)
        csv_content = ServiceRelatorioMovimentacao.exportar_csv(relatorio)
        
        # Criar nome do arquivo baseado no período
        filename = "movimentacoes_estoque"
        if data_inicio:
            filename += f"_{data_inicio.strftime('%Y%m%d')}"
        if data_fim:
            filename += f"_a_{data_fim.strftime('%Y%m%d')}"
        filename += ".csv"
        
        return StreamingResponse(
            io.StringIO(csv_content),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao exportar relatório: {str(e)}"
        )

@router.get("/por-produto/{produto_nome}")
def obter_movimentacoes_por_produto(
    produto_nome: str,
    data_inicio: Optional[date] = Query(None, description="Data inicial do período"),
    data_fim: Optional[date] = Query(None, description="Data final do período"),
    db: Session = Depends(get_db),
):
    """
    Obtém movimentações específicas de um produto.
    
    **Útil para rastrear histórico de um produto específico.**
    """
    try:
        filtros = FiltroRelatorioMovimentacao(
            produto_nome=produto_nome,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        
        relatorio = ServiceRelatorioMovimentacao.gerar_relatorio(db, filtros)
        return relatorio
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter movimentações do produto: {str(e)}"
        )

@router.get("/por-armazem/{armazem_id}")
def obter_movimentacoes_por_armazem(
    armazem_id: int,
    data_inicio: Optional[date] = Query(None, description="Data inicial do período"),
    data_fim: Optional[date] = Query(None, description="Data final do período"),
    db: Session = Depends(get_db),
):
    """
    Obtém movimentações específicas de um armazém.
    
    **Útil para analisar atividade por local de estoque.**
    """
    try:
        filtros = FiltroRelatorioMovimentacao(
            armazem_id=armazem_id,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        
        relatorio = ServiceRelatorioMovimentacao.gerar_relatorio(db, filtros)
        return relatorio
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter movimentações do armazém: {str(e)}"
        )

@router.get("/por-funcionario/{funcionario_id}")
def obter_movimentacoes_por_funcionario(
    funcionario_id: int,
    data_inicio: Optional[date] = Query(None, description="Data inicial do período"),
    data_fim: Optional[date] = Query(None, description="Data final do período"),
    db: Session = Depends(get_db),
):
    """
    Obtém movimentações realizadas por um funcionário específico.
    
    **Útil para auditoria e análise de desempenho.**
    """
    try:
        filtros = FiltroRelatorioMovimentacao(
            funcionario_id=funcionario_id,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        
        relatorio = ServiceRelatorioMovimentacao.gerar_relatorio(db, filtros)
        return relatorio
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter movimentações do funcionário: {str(e)}"
        )
