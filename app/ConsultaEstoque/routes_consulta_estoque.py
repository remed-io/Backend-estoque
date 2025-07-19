from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.settings import get_db
from app.ConsultaEstoque.schema_consulta_estoque import (
    ConsultaEstoqueRead,
    FiltroConsultaEstoque,
    ResumoEstoque,
    EstoqueDetalhado,
    TipoProduto
)
from app.ConsultaEstoque import service_consulta_estoque

router = APIRouter(prefix="/consulta-estoque", tags=["Consulta de Estoque"])

@router.get("/resumo", response_model=ResumoEstoque)
def get_resumo_estoque(
    db: Session = Depends(get_db),
):
    """Obter resumo geral do estoque"""
    return service_consulta_estoque.gerar_resumo_estoque(db)

@router.get("/", response_model=List[ConsultaEstoqueRead])
def consultar_estoque(
    produto_nome: str = Query(None, description="Filtrar por nome do produto"),
    codigo_barras: str = Query(None, description="Filtrar por código de barras"),
    tipo_produto: TipoProduto = Query(None, description="Filtrar por tipo de produto"),
    fornecedor_id: int = Query(None, description="Filtrar por fornecedor"),
    armazem_id: int = Query(None, description="Filtrar por armazém"),
    vencidos: bool = Query(None, description="Mostrar apenas produtos vencidos"),
    dias_vencimento: int = Query(None, description="Produtos que vencem em X dias", ge=0),
    estoque_baixo: bool = Query(None, description="Mostrar apenas itens com estoque baixo"),
    estoque_critico: bool = Query(None, description="Mostrar apenas itens com estoque crítico"),
    quantidade_min: int = Query(None, description="Filtrar por quantidade mínima", ge=0),
    quantidade_max: int = Query(None, description="Filtrar por quantidade máxima", ge=0),
    skip: int = Query(0, description="Pular N registros", ge=0),
    limit: int = Query(100, description="Limitar resultados", ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Consultar estoque com filtros"""
    
    filtros = FiltroConsultaEstoque(
        produto_nome=produto_nome,
        codigo_barras=codigo_barras,
        tipo_produto=tipo_produto,
        fornecedor_id=fornecedor_id,
        armazem_id=armazem_id,
        vencidos=vencidos,
        dias_vencimento=dias_vencimento,
        estoque_baixo=estoque_baixo,
        estoque_critico=estoque_critico,
        quantidade_min=quantidade_min,
        quantidade_max=quantidade_max,
        status=None
    )
    
    return service_consulta_estoque.consultar_estoque(db, filtros, skip, limit)
@router.get("/detalhado", response_model=EstoqueDetalhado)
def consultar_estoque_detalhado(
    produto_nome: str = Query(None, description="Filtrar por nome do produto"),
    codigo_barras: str = Query(None, description="Filtrar por código de barras"),
    tipo_produto: TipoProduto = Query(None, description="Filtrar por tipo de produto"),
    fornecedor_id: int = Query(None, description="Filtrar por fornecedor"),
    armazem_id: int = Query(None, description="Filtrar por armazém"),
    vencidos: bool = Query(None, description="Mostrar apenas produtos vencidos"),
    dias_vencimento: int = Query(None, description="Produtos que vencem em X dias", ge=0),
    estoque_baixo: bool = Query(None, description="Mostrar apenas itens com estoque baixo"),
    estoque_critico: bool = Query(None, description="Mostrar apenas itens com estoque crítico"),
    quantidade_min: int = Query(None, description="Filtrar por quantidade mínima", ge=0),
    quantidade_max: int = Query(None, description="Filtrar por quantidade máxima", ge=0),
    skip: int = Query(0, description="Pular N registros", ge=0),
    limit: int = Query(100, description="Limitar resultados", ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Consultar estoque detalhado com resumo"""
    
    filtros = FiltroConsultaEstoque(
        produto_nome=produto_nome,
        codigo_barras=codigo_barras,
        tipo_produto=tipo_produto,
        fornecedor_id=fornecedor_id,
        armazem_id=armazem_id,
        vencidos=vencidos,
        dias_vencimento=dias_vencimento,
        estoque_baixo=estoque_baixo,
        estoque_critico=estoque_critico,
        quantidade_min=quantidade_min,
        quantidade_max=quantidade_max,
        status=None
    )
    
    return service_consulta_estoque.consultar_estoque_detalhado(db, filtros, skip, limit)

@router.get("/vencidos", response_model=List[ConsultaEstoqueRead])
def consultar_produtos_vencidos(
    dias_limite: int = Query(0, description="Dias limite para vencimento (0=já vencidos)", ge=0),
    db: Session = Depends(get_db),
):
    """Consultar produtos vencidos ou próximos do vencimento"""
    return service_consulta_estoque.consultar_produtos_vencidos(db, dias_limite)

@router.get("/critico", response_model=List[ConsultaEstoqueRead])
def consultar_estoque_critico(
    db: Session = Depends(get_db),
):
    """Consultar itens com estoque crítico ou baixo"""
    return service_consulta_estoque.consultar_estoque_critico(db)

@router.get("/por-produto/{produto_id}", response_model=List[ConsultaEstoqueRead])
def consultar_estoque_por_produto(
    produto_id: int,
    db: Session = Depends(get_db),
):
    """Consultar estoque de um produto específico em todos os armazéns"""
    # Buscar todos os itens deste produto
    filtros = FiltroConsultaEstoque(
        produto_nome=None,
        codigo_barras=None,
        tipo_produto=None,
        fornecedor_id=None,
        armazem_id=None,
        vencidos=None,
        dias_vencimento=None,
        estoque_baixo=None,
        estoque_critico=None,
        quantidade_min=None,
        quantidade_max=None,
        status=None
    )
    todos_itens = service_consulta_estoque.consultar_estoque(db, filtros, 0, 1000)
    itens_produto = [item for item in todos_itens if item.produto_id == produto_id]
    
    return itens_produto

@router.get("/por-armazem/{armazem_id}", response_model=List[ConsultaEstoqueRead])
def consultar_estoque_por_armazem(
    armazem_id: int,
    skip: int = Query(0, description="Pular N registros", ge=0),
    limit: int = Query(100, description="Limitar resultados", ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Consultar todos os itens de um armazém específico"""
    # Filtrar por armazém específico
    filtros = FiltroConsultaEstoque(
        produto_nome=None,
        codigo_barras=None,
        tipo_produto=None,
        fornecedor_id=None,
        armazem_id=armazem_id,
        vencidos=None,
        dias_vencimento=None,
        estoque_baixo=None,
        estoque_critico=None,
        quantidade_min=None,
        quantidade_max=None,
        status=None
    )
    return service_consulta_estoque.consultar_estoque(db, filtros, skip, limit)

@router.get("/por-item-estoque/{item_estoque_id}", response_model=List[ConsultaEstoqueRead])
def consultar_estoque_por_item_estoque(
    item_estoque_id: int,
    db: Session = Depends(get_db),
):
    """Consultar estoque de um item específico por seu item_estoque_id"""
    # Reutiliza a consulta geral e filtra pelo item_estoque_id
    todos = service_consulta_estoque.consultar_estoque(db, None, 0, 1000)
    return [item for item in todos if item.item_estoque_id == item_estoque_id]
