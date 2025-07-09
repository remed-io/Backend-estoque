from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import date, datetime, timedelta
import csv
import io
import json

from app.Relatorios.schema_relatorio_vencimento import (
    RelatorioVencimento,
    ResumoVencimento,
    ItemVencimento,
    FiltroRelatorioVencimento,
    StatusVencimento,
    TipoVencimento,
    ExportacaoConfig
)
from app.ItemEstoque.model_item_estoque import ItemEstoque
from app.ItemArmazenado.model_item_armazenado import ItemArmazenado
from app.Armazem.model_armazem import Armazem
from app.Fornecedor.model_fornecedor import Fornecedor

def _determinar_status_vencimento(dias_para_vencimento: int) -> StatusVencimento:
    """Determina o status baseado nos dias para vencimento"""
    if dias_para_vencimento < 0:
        return StatusVencimento.VENCIDO
    elif dias_para_vencimento <= 3:
        return StatusVencimento.CRITICO
    elif dias_para_vencimento <= 15:
        return StatusVencimento.ATENCAO
    else:
        return StatusVencimento.NORMAL

def gerar_relatorio_vencimento(db: Session, filtros: FiltroRelatorioVencimento) -> RelatorioVencimento:
    """Gera relatório completo de produtos vencidos e próximos do vencimento"""
    
    hoje = date.today()
    data_limite = hoje + timedelta(days=filtros.dias_limite)
    
    # Query base com joins
    query = db.query(
        ItemEstoque.id.label('item_estoque_id'),
        ItemEstoque.produto_id,
        ItemEstoque.produto_nome,
        ItemEstoque.tipo_produto,
        ItemEstoque.codigo_barras,
        ItemEstoque.lote,
        ItemEstoque.data_validade,
        ItemEstoque.preco.label('valor_unitario'),
        ItemEstoque.fornecedor_id,
        Fornecedor.nome.label('fornecedor_nome'),
        ItemArmazenado.armazem_id,
        Armazem.local_armazem.label('armazem_nome'),
        ItemArmazenado.quantidade.label('quantidade_atual'),
        # Calcular dias para vencimento
        (func.extract('day', ItemEstoque.data_validade - func.current_date())).label('dias_para_vencimento')
    ).join(
        ItemArmazenado, ItemEstoque.id == ItemArmazenado.item_estoque_id
    ).join(
        Armazem, ItemArmazenado.armazem_id == Armazem.id
    ).join(
        Fornecedor, ItemEstoque.fornecedor_id == Fornecedor.id
    )
    
    # Aplicar filtros básicos
    if filtros.incluir_vencidos:
        # Incluir vencidos + que vencem até X dias
        query = query.filter(ItemEstoque.data_validade <= data_limite)
    else:
        # Apenas produtos que ainda não venceram mas vão vencer
        query = query.filter(
            and_(
                ItemEstoque.data_validade > hoje,
                ItemEstoque.data_validade <= data_limite
            )
        )
    
    # Filtros opcionais
    if filtros.armazem_id:
        query = query.filter(ItemArmazenado.armazem_id == filtros.armazem_id)
    
    if filtros.fornecedor_id:
        query = query.filter(ItemEstoque.fornecedor_id == filtros.fornecedor_id)
    
    if filtros.tipo_produto:
        query = query.filter(ItemEstoque.tipo_produto == filtros.tipo_produto)
    
    if filtros.apenas_com_estoque:
        query = query.filter(ItemArmazenado.quantidade > 0)
    
    if filtros.valor_minimo:
        query = query.filter(ItemEstoque.preco >= filtros.valor_minimo)
    
    # Executar query
    resultados = query.all()
    
    # Processar resultados
    itens_vencimento = []
    contadores = {
        'total_itens': 0,
        'vencidos': 0,
        'vence_hoje': 0,
        'vence_amanha': 0,
        'vence_3_dias': 0,
        'vence_7_dias': 0,
        'vence_15_dias': 0,
        'vence_30_dias': 0,
        'valor_vencidos': 0.0,
        'valor_criticos': 0.0,
        'valor_atencao': 0.0
    }
    
    for resultado in resultados:
        dias_para_vencimento = int(resultado.dias_para_vencimento or 0)
        status_vencimento = _determinar_status_vencimento(dias_para_vencimento)
        valor_total = resultado.valor_unitario * resultado.quantidade_atual
        
        item = ItemVencimento(
            item_estoque_id=resultado.item_estoque_id,
            produto_id=resultado.produto_id,
            produto_nome=resultado.produto_nome,
            tipo_produto=resultado.tipo_produto,
            codigo_barras=resultado.codigo_barras,
            lote=resultado.lote,
            data_validade=resultado.data_validade,
            dias_para_vencimento=dias_para_vencimento,
            status_vencimento=status_vencimento,
            quantidade_atual=resultado.quantidade_atual,
            valor_unitario=resultado.valor_unitario,
            valor_total=valor_total,
            fornecedor_id=resultado.fornecedor_id,
            fornecedor_nome=resultado.fornecedor_nome,
            armazem_id=resultado.armazem_id,
            armazem_nome=resultado.armazem_nome
        )
        
        itens_vencimento.append(item)
        
        # Atualizar contadores
        contadores['total_itens'] += 1
        
        if dias_para_vencimento < 0:
            contadores['vencidos'] += 1
            contadores['valor_vencidos'] += valor_total
        elif dias_para_vencimento == 0:
            contadores['vence_hoje'] += 1
        elif dias_para_vencimento == 1:
            contadores['vence_amanha'] += 1
        elif dias_para_vencimento <= 3:
            contadores['vence_3_dias'] += 1
        elif dias_para_vencimento <= 7:
            contadores['vence_7_dias'] += 1
        elif dias_para_vencimento <= 15:
            contadores['vence_15_dias'] += 1
        elif dias_para_vencimento <= 30:
            contadores['vence_30_dias'] += 1
        
        # Valores por status
        if status_vencimento == StatusVencimento.CRITICO:
            contadores['valor_criticos'] += valor_total
        elif status_vencimento == StatusVencimento.ATENCAO:
            contadores['valor_atencao'] += valor_total
    
    # Criar resumo
    resumo = ResumoVencimento(
        total_itens_analisados=contadores['total_itens'],
        produtos_vencidos=contadores['vencidos'],
        produtos_vence_hoje=contadores['vence_hoje'],
        produtos_vence_amanha=contadores['vence_amanha'],
        produtos_vence_3_dias=contadores['vence_3_dias'],
        produtos_vence_7_dias=contadores['vence_7_dias'],
        produtos_vence_15_dias=contadores['vence_15_dias'],
        produtos_vence_30_dias=contadores['vence_30_dias'],
        valor_total_vencidos=contadores['valor_vencidos'],
        valor_total_criticos=contadores['valor_criticos'],
        valor_total_atencao=contadores['valor_atencao']
    )
    
    # Montar relatório final
    relatorio = RelatorioVencimento(
        data_geracao=hoje,
        parametros=filtros.dict(),
        resumo=resumo,
        itens=itens_vencimento
    )
    
    return relatorio

def exportar_relatorio_csv(relatorio: RelatorioVencimento) -> str:
    """Exporta relatório para formato CSV"""
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Cabeçalho do CSV
    writer.writerow([
        'ID Item', 'Produto ID', 'Nome Produto', 'Tipo', 'Código Barras',
        'Lote', 'Data Validade', 'Dias p/ Vencimento', 'Status',
        'Quantidade', 'Valor Unitário', 'Valor Total',
        'Fornecedor', 'Armazém'
    ])
    
    # Dados
    for item in relatorio.itens:
        writer.writerow([
            item.item_estoque_id,
            item.produto_id,
            item.produto_nome,
            item.tipo_produto,
            item.codigo_barras,
            item.lote,
            item.data_validade.strftime('%d/%m/%Y'),
            item.dias_para_vencimento,
            item.status_vencimento.value,
            item.quantidade_atual,
            f'{item.valor_unitario:.2f}',
            f'{item.valor_total:.2f}',
            item.fornecedor_nome,
            item.armazem_nome
        ])
    
    return output.getvalue()

def obter_produtos_vencidos_hoje(db: Session) -> List[ItemVencimento]:
    """Retorna produtos que vencem hoje"""
    filtros = FiltroRelatorioVencimento(
        dias_limite=0,
        incluir_vencidos=False
    )
    relatorio = gerar_relatorio_vencimento(db, filtros)
    return [item for item in relatorio.itens if item.dias_para_vencimento == 0]

def obter_produtos_criticos(db: Session, dias_limite: int = 3) -> List[ItemVencimento]:
    """Retorna produtos em situação crítica (vencimento próximo)"""
    filtros = FiltroRelatorioVencimento(
        dias_limite=dias_limite,
        incluir_vencidos=True
    )
    relatorio = gerar_relatorio_vencimento(db, filtros)
    return [item for item in relatorio.itens if item.status_vencimento in [StatusVencimento.VENCIDO, StatusVencimento.CRITICO]]
