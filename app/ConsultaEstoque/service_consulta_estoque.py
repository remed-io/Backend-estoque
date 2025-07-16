from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, case, cast, Date
from typing import List, Optional
from datetime import datetime, timedelta, date
import logging

from app.ConsultaEstoque.schema_consulta_estoque import (
    ConsultaEstoqueRead, 
    FiltroConsultaEstoque, 
    ResumoEstoque, 
    EstoqueDetalhado,
    StatusEstoque,
    TipoProduto
)
from app.ItemEstoque.model_item_estoque import ItemEstoque
from app.ItemArmazenado.model_item_armazenado import ItemArmazenado
from app.Armazem.model_armazem import Armazem
from app.Fornecedor.model_fornecedor import Fornecedor
from app.Medicamento.model_medicamento import Medicamento
from app.CuidadoPessoal.model_cuidado_pessoal import CuidadoPessoal
from app.SuplementoAlimentar.model_suplemento_alimentar import SuplementoAlimentar

def _determinar_status(quantidade_atual: int, quantidade_minima: int, dias_para_vencimento: int) -> StatusEstoque:
    """Determina o status do item baseado nas regras de negócio"""
    hoje = date.today()
    
    # Produto vencido
    if dias_para_vencimento < 0:
        return StatusEstoque.VENCIDO
    
    # Produto próximo do vencimento (30 dias)
    if dias_para_vencimento <= 30:
        return StatusEstoque.PROXIMO_VENCIMENTO
    
    # Estoque crítico (quantidade = 0)
    if quantidade_atual == 0:
        return StatusEstoque.ESTOQUE_CRITICO
    
    # Estoque baixo (quantidade <= mínima)
    if quantidade_atual <= quantidade_minima:
        return StatusEstoque.ESTOQUE_BAIXO
    
    return StatusEstoque.NORMAL

def consultar_estoque(db: Session, filtros: FiltroConsultaEstoque = None, skip: int = 0, limit: int = 100) -> List[ConsultaEstoqueRead]:
    """Consulta o estoque com filtros aplicados"""
    
    # Query base com joins
    query = db.query(
        ItemEstoque.id.label('item_estoque_id'),
        ItemEstoque.produto_id,
        ItemEstoque.produto_nome,
        ItemEstoque.tipo_produto,
        ItemEstoque.codigo_barras,
        ItemEstoque.preco,
        ItemEstoque.data_validade,
        ItemEstoque.lote,
        ItemEstoque.fornecedor_id,
        Fornecedor.nome.label('fornecedor_nome'),
        ItemArmazenado.armazem_id,
        Armazem.local_armazem.label('armazem_local'),
        ItemArmazenado.quantidade.label('quantidade_atual'),
        Armazem.quantidade_minima,
        # Calcular dias para vencimento: converte timestamp para date e subtrai current_date (resulta em integer)
        (cast(ItemEstoque.data_validade, Date) - func.current_date()).label('dias_para_vencimento')
    ).join(
        ItemArmazenado, ItemEstoque.id == ItemArmazenado.item_estoque_id
    ).join(
        Armazem, ItemArmazenado.armazem_id == Armazem.id
    ).join(
        Fornecedor, ItemEstoque.fornecedor_id == Fornecedor.id
    )
    
    # Aplicar filtros se fornecidos
    if filtros:
        # Filtro por nome do produto
        if filtros.produto_nome:
            query = query.filter(ItemEstoque.produto_nome.ilike(f"%{filtros.produto_nome}%"))
        
        # Filtro por código de barras
        if filtros.codigo_barras:
            query = query.filter(ItemEstoque.codigo_barras == filtros.codigo_barras)
        
        # Filtro por tipo de produto
        if filtros.tipo_produto:
            query = query.filter(ItemEstoque.tipo_produto == filtros.tipo_produto.value)
        
        # Filtro por fornecedor
        if filtros.fornecedor_id:
            query = query.filter(ItemEstoque.fornecedor_id == filtros.fornecedor_id)
        
        # Filtro por armazém
        if filtros.armazem_id:
            query = query.filter(ItemArmazenado.armazem_id == filtros.armazem_id)
        
        # Filtro de produtos vencidos
        if filtros.vencidos:
            query = query.filter(ItemEstoque.data_validade < func.current_date())
        
        # Filtro por dias para vencimento
        if filtros.dias_vencimento is not None:
            data_limite = datetime.now().date() + timedelta(days=filtros.dias_vencimento)
            query = query.filter(ItemEstoque.data_validade <= data_limite)
        
        # Filtro de estoque baixo
        if filtros.estoque_baixo:
            query = query.filter(ItemArmazenado.quantidade <= Armazem.quantidade_minima)
        
        # Filtro de estoque crítico
        if filtros.estoque_critico:
            query = query.filter(ItemArmazenado.quantidade == 0)
        
        # Filtro por quantidade mínima
        if filtros.quantidade_min is not None:
            query = query.filter(ItemArmazenado.quantidade >= filtros.quantidade_min)
        
        # Filtro por quantidade máxima
        if filtros.quantidade_max is not None:
            query = query.filter(ItemArmazenado.quantidade <= filtros.quantidade_max)
    
    # Aplicar paginação
    resultados = query.offset(skip).limit(limit).all()
    
    # Converter para o schema de resposta
    itens_estoque = []
    hoje = date.today()
    
    for resultado in resultados:
        dias_para_vencimento = resultado.dias_para_vencimento
        status = _determinar_status(
            resultado.quantidade_atual, 
            resultado.quantidade_minima, 
            dias_para_vencimento
        )
        
        # Se há filtro de status específico, aplicar
        if filtros and filtros.status and status not in filtros.status:
            continue
        
        item = ConsultaEstoqueRead(
            item_estoque_id=resultado.item_estoque_id,
            produto_id=resultado.produto_id,
            produto_nome=resultado.produto_nome,
            tipo_produto=TipoProduto(resultado.tipo_produto),
            codigo_barras=resultado.codigo_barras,
            preco=resultado.preco,
            data_validade=resultado.data_validade,
            lote=resultado.lote,
            fornecedor_id=resultado.fornecedor_id,
            fornecedor_nome=resultado.fornecedor_nome,
            armazem_id=resultado.armazem_id,
            armazem_local=resultado.armazem_local,
            quantidade_atual=resultado.quantidade_atual,
            quantidade_minima=resultado.quantidade_minima,
            status=status,
            dias_para_vencimento=int(dias_para_vencimento) if dias_para_vencimento is not None else None
        )
        itens_estoque.append(item)
    
    return itens_estoque

def gerar_resumo_estoque(db: Session) -> ResumoEstoque:
    """Gera resumo geral do estoque"""
    
    # Consultar todos os itens para calcular estatísticas
    todos_itens = consultar_estoque(db, limit=10000)  # Limite alto para pegar todos
    
    total_itens = len(todos_itens)
    produtos_diferentes = len(set(item.produto_id for item in todos_itens))
    
    # Contar por status
    vencidos = sum(1 for item in todos_itens if item.status == StatusEstoque.VENCIDO)
    proximo_vencimento = sum(1 for item in todos_itens if item.status == StatusEstoque.PROXIMO_VENCIMENTO)
    estoque_baixo = sum(1 for item in todos_itens if item.status == StatusEstoque.ESTOQUE_BAIXO)
    estoque_critico = sum(1 for item in todos_itens if item.status == StatusEstoque.ESTOQUE_CRITICO)
    
    # Calcular valor total
    valor_total = sum(item.preco * item.quantidade_atual for item in todos_itens)
    
    return ResumoEstoque(
        total_itens=total_itens,
        total_produtos_diferentes=produtos_diferentes,
        produtos_vencidos=vencidos,
        produtos_proximo_vencimento=proximo_vencimento,
        produtos_estoque_baixo=estoque_baixo,
        produtos_estoque_critico=estoque_critico,
        valor_total_estoque=valor_total
    )

def consultar_estoque_detalhado(db: Session, filtros: FiltroConsultaEstoque = None, skip: int = 0, limit: int = 100) -> EstoqueDetalhado:
    """Consulta detalhada do estoque com resumo"""
    
    resumo = gerar_resumo_estoque(db)
    itens = consultar_estoque(db, filtros, skip, limit)
    
    return EstoqueDetalhado(
        resumo=resumo,
        itens=itens
    )

def consultar_produtos_vencidos(db: Session, dias_limite: int = 0) -> List[ConsultaEstoqueRead]:
    """Consulta produtos vencidos ou próximos do vencimento"""
    
    filtros = FiltroConsultaEstoque(
        dias_vencimento=dias_limite
    )
    
    return consultar_estoque(db, filtros)

def consultar_estoque_critico(db: Session) -> List[ConsultaEstoqueRead]:
    """Consulta itens com estoque crítico ou baixo"""
    
    filtros = FiltroConsultaEstoque(
        status=[StatusEstoque.ESTOQUE_CRITICO, StatusEstoque.ESTOQUE_BAIXO]
    )
    
    return consultar_estoque(db, filtros)
