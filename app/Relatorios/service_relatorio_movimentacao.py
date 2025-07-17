from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional
from datetime import datetime, date
import csv
import io

from app.MovimentacaoEstoque.model_movimentacao_estoque import MovimentacaoEstoque
from app.ItemEstoque.model_item_estoque import ItemEstoque
from app.Medicamento.model_medicamento import Medicamento
from app.CuidadoPessoal.model_cuidado_pessoal import CuidadoPessoal
from app.SuplementoAlimentar.model_suplemento_alimentar import SuplementoAlimentar
from app.Armazem.model_armazem import Armazem


from .schema_relatorio_movimentacao import (
    FiltroRelatorioMovimentacao,
    MovimentacaoResumo,
    EstatisticasMovimentacao,
    RelatorioMovimentacao,
    TipoMovimentacao
)

class ServiceRelatorioMovimentacao:
    
    @staticmethod
    def gerar_relatorio(db: Session, filtros: FiltroRelatorioMovimentacao) -> RelatorioMovimentacao:
        """
        Gera relatório completo de movimentações com base nos filtros
        """
        
        # Query base com joins necessários
        query = db.query(MovimentacaoEstoque).options(
            joinedload(MovimentacaoEstoque.item).joinedload(ItemEstoque.medicamento),
            joinedload(MovimentacaoEstoque.item).joinedload(ItemEstoque.cuidado_pessoal),
            joinedload(MovimentacaoEstoque.item).joinedload(ItemEstoque.suplemento_alimentar),
            joinedload(MovimentacaoEstoque.armazem),
            joinedload(MovimentacaoEstoque.responsavel)
        )
        
        # Aplicar filtros
        query = ServiceRelatorioMovimentacao._aplicar_filtros(query, filtros)
        
        # Ordenar por data decrescente
        query = query.order_by(desc(MovimentacaoEstoque.data_movimentacao))
        
        # Executar query
        movimentacoes = query.all()
        
        # Converter para schema de resumo
        movimentacoes_resumo = [
            ServiceRelatorioMovimentacao._converter_para_resumo(mov) 
            for mov in movimentacoes
        ]
        
        # Calcular estatísticas
        estatisticas = ServiceRelatorioMovimentacao._calcular_estatisticas(
            movimentacoes, filtros
        )
        
        return RelatorioMovimentacao(
            movimentacoes=movimentacoes_resumo,
            estatisticas=estatisticas,
            filtros_aplicados=filtros
        )
    
    @staticmethod
    def _aplicar_filtros(query, filtros: FiltroRelatorioMovimentacao):
        """Aplica filtros à query de movimentações"""
        
        if filtros.data_inicio:
            query = query.filter(
                func.date(MovimentacaoEstoque.data_movimentacao) >= filtros.data_inicio
            )
        
        if filtros.data_fim:
            query = query.filter(
                func.date(MovimentacaoEstoque.data_movimentacao) <= filtros.data_fim
            )
        
        if filtros.tipo:
            query = query.filter(
                MovimentacaoEstoque.tipo == filtros.tipo.value
            )
        
        if filtros.armazem_id:
            query = query.filter(
                MovimentacaoEstoque.armazem_id == filtros.armazem_id
            )
        
        if filtros.funcionario_id:
            query = query.filter(
                MovimentacaoEstoque.responsavel_id == filtros.funcionario_id
            )
        
        if filtros.item_id:
            query = query.filter(
                MovimentacaoEstoque.item_id == filtros.item_id
            )
        
        if filtros.produto_nome:
            # Buscar em todas as categorias de produto
            query = query.join(ItemEstoque).filter(
                or_(
                    and_(
                        ItemEstoque.medicamento_id.isnot(None),
                        ItemEstoque.medicamento.has(
                            Medicamento.nome.ilike(f"%{filtros.produto_nome}%")
                        )
                    ),
                    and_(
                        ItemEstoque.cuidado_pessoal_id.isnot(None),
                        ItemEstoque.cuidado_pessoal.has(
                            CuidadoPessoal.nome.ilike(f"%{filtros.produto_nome}%")
                        )
                    ),
                    and_(
                        ItemEstoque.suplemento_alimentar_id.isnot(None),
                        ItemEstoque.suplemento_alimentar.has(
                            SuplementoAlimentar.nome.ilike(f"%{filtros.produto_nome}%")
                        )
                    )
                )
            )
        
        return query
    
    @staticmethod
    def _converter_para_resumo(movimentacao: MovimentacaoEstoque) -> MovimentacaoResumo:
        """Converte modelo MovimentacaoEstoque para schema MovimentacaoResumo"""
        
        # Determinar nome do produto baseado na categoria
        produto_nome = ""
        if movimentacao.item.medicamento:
            produto_nome = movimentacao.item.medicamento.nome
        elif movimentacao.item.cuidado_pessoal:
            produto_nome = movimentacao.item.cuidado_pessoal.nome
        elif movimentacao.item.suplemento_alimentar:
            produto_nome = movimentacao.item.suplemento_alimentar.nome
        
        return MovimentacaoResumo(
            id=movimentacao.id,
            data=movimentacao.data_movimentacao,
            tipo=movimentacao.tipo,
            quantidade=movimentacao.quantidade,
            
            # Dados do item
            item_id=movimentacao.item.id,
            produto_nome=produto_nome,
            lote=movimentacao.item.lote,
            data_vencimento=movimentacao.item.data_vencimento,
            preco_custo=float(movimentacao.item.preco),
            
            # Dados do armazém
            armazem_id=movimentacao.armazem.id,
            armazem_nome=movimentacao.armazem.nome,
            
            # Dados do funcionário
            funcionario_id=movimentacao.responsavel.id,
            funcionario_nome=movimentacao.responsavel.nome,
            
            # Dados específicos para saída
            cpf_comprador=movimentacao.cpf_comprador,
            nome_comprador=movimentacao.nome_comprador,
            receita_digital=movimentacao.receita_digital
        )
    
    @staticmethod
    def _calcular_estatisticas(
        movimentacoes: List[MovimentacaoEstoque], 
        filtros: FiltroRelatorioMovimentacao
    ) -> EstatisticasMovimentacao:
        """Calcula estatísticas das movimentações"""
        
        total_movimentacoes = len(movimentacoes)
        
        entradas = [m for m in movimentacoes if m.tipo.lower() == "entrada"]
        saidas = [m for m in movimentacoes if m.tipo.lower() == "saida"]
        
        total_entradas = len(entradas)
        total_saidas = len(saidas)
        
        quantidade_total_entrada = sum(m.quantidade for m in entradas)
        quantidade_total_saida = sum(m.quantidade for m in saidas)
        
        valor_total_entrada = sum(
            m.quantidade * float(m.item.preco) for m in entradas
        )
        valor_total_saida = sum(
            m.quantidade * float(m.item.preco) for m in saidas
        )
        
        return EstatisticasMovimentacao(
            total_movimentacoes=total_movimentacoes,
            total_entradas=total_entradas,
            total_saidas=total_saidas,
            quantidade_total_entrada=quantidade_total_entrada,
            quantidade_total_saida=quantidade_total_saida,
            valor_total_entrada=valor_total_entrada,
            valor_total_saida=valor_total_saida,
            periodo_inicio=filtros.data_inicio,
            periodo_fim=filtros.data_fim
        )
    
    @staticmethod
    def obter_resumo_periodo(db: Session, data_inicio: Optional[date], data_fim: Optional[date]) -> EstatisticasMovimentacao:
        """Obtém apenas as estatísticas de movimentações para um período"""
        filtros = FiltroRelatorioMovimentacao(
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        rel = ServiceRelatorioMovimentacao.gerar_relatorio(db, filtros)
        est = rel.estatisticas
        est.periodo_inicio = data_inicio
        est.periodo_fim = data_fim
        return est

    @staticmethod
    def obter_item_mais_vendido(db: Session, data_inicio: date, data_fim: date) -> Optional[str]:
        """Calcula o item mais retirado (mais vendido) no período"""
        from sqlalchemy import func, desc
        # somar quantidades de saida por item
        subq = db.query(
            MovimentacaoEstoque.item_estoque_id.label('item_estoque_id'),
            func.sum(MovimentacaoEstoque.quantidade).label('total')
        ).filter(
            func.date(MovimentacaoEstoque.data_movimentacao) >= data_inicio,
            func.date(MovimentacaoEstoque.data_movimentacao) <= data_fim,
            MovimentacaoEstoque.tipo == 'saida'
        ).group_by(MovimentacaoEstoque.item_estoque_id).order_by(desc('total')).limit(1).first()
        if not subq:
            return None
        item_id = subq.item_estoque_id
        # buscar nome do produto
        from app.ItemEstoque.model_item_estoque import ItemEstoque
        item = db.query(ItemEstoque).options(
            joinedload(ItemEstoque.medicamento),
            joinedload(ItemEstoque.cuidado_pessoal),
            joinedload(ItemEstoque.suplemento_alimentar)
        ).filter(ItemEstoque.id == item_id).first()
        if not item:
            return None
        # determina nome
        if item.medicamento:
            return item.medicamento.nome
        if item.cuidado_pessoal:
            return item.cuidado_pessoal.nome
        if item.suplemento_alimentar:
            return item.suplemento_alimentar.nome
        return None
    
    @staticmethod
    def exportar_csv(relatorio: RelatorioMovimentacao) -> str:
        """
        Exporta relatório para formato CSV
        Returns: string com conteúdo CSV
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Cabeçalho
        headers = [
            "ID", "Data", "Tipo", "Quantidade", "Produto", "Lote", "Vencimento",
            "Preço Custo", "Valor Total", "Armazém", "Funcionário",
            "CPF Comprador", "Nome Comprador", "Receita Digital"
        ]
        writer.writerow(headers)
        
        # Dados
        for mov in relatorio.movimentacoes:
            valor_total = mov.quantidade * mov.preco_custo
            
            row = [
                mov.id,
                mov.data.strftime("%d/%m/%Y %H:%M"),
                mov.tipo,
                mov.quantidade,
                mov.produto_nome,
                mov.lote,
                mov.data_vencimento.strftime("%d/%m/%Y"),
                f"R$ {mov.preco_custo:.2f}",
                f"R$ {valor_total:.2f}",
                mov.armazem_nome,
                mov.funcionario_nome,
                mov.cpf_comprador or "",
                mov.nome_comprador or "",
                mov.receita_digital or ""
            ]
            writer.writerow(row)
        
        # Adicionar estatísticas se solicitado
        writer.writerow([])  # Linha vazia
        writer.writerow(["ESTATÍSTICAS"])
        writer.writerow(["Total de Movimentações", relatorio.estatisticas.total_movimentacoes])
        writer.writerow(["Total de Entradas", relatorio.estatisticas.total_entradas])
        writer.writerow(["Total de Saídas", relatorio.estatisticas.total_saidas])
        writer.writerow(["Quantidade Total Entrada", relatorio.estatisticas.quantidade_total_entrada])
        writer.writerow(["Quantidade Total Saída", relatorio.estatisticas.quantidade_total_saida])
        writer.writerow(["Valor Total Entrada", f"R$ {relatorio.estatisticas.valor_total_entrada:.2f}"])
        writer.writerow(["Valor Total Saída", f"R$ {relatorio.estatisticas.valor_total_saida:.2f}"])
        
        return output.getvalue()
    
    @staticmethod
    def obter_resumo_periodo(
        db: Session, 
        data_inicio: Optional[date] = None, 
        data_fim: Optional[date] = None
    ) -> EstatisticasMovimentacao:
        """
        Obtém resumo rápido das movimentações para um período
        """
        filtros = FiltroRelatorioMovimentacao(
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        
        query = db.query(MovimentacaoEstoque).options(
            joinedload(MovimentacaoEstoque.item)
        )
        
        query = ServiceRelatorioMovimentacao._aplicar_filtros(query, filtros)
        movimentacoes = query.all()
        
        return ServiceRelatorioMovimentacao._calcular_estatisticas(movimentacoes, filtros)
