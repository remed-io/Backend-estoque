from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func, case
from typing import List, Optional
from datetime import datetime, timedelta, date
import logging

from app.Alertas.model_alertas import AlertaEstoque, NotificacaoAlerta, ConfiguracaoAlertas
from app.Alertas.schema_alertas import (
    AlertaEstoque as AlertaSchema,
    AlertaCritico,
    ResumoAlertas,
    FiltroAlertas,
    RelatorioAlertas,
    TipoAlerta,
    PrioridadeAlerta
)
from app.ItemArmazenado.model_item_armazenado import ItemArmazenado
from app.ItemEstoque.model_item_estoque import ItemEstoque
from app.Armazem.model_armazem import Armazem
from app.Medicamento.model_medicamento import Medicamento
from app.CuidadoPessoal.model_cuidado_pessoal import CuidadoPessoal
from app.SuplementoAlimentar.model_suplemento_alimentar import SuplementoAlimentar

logger = logging.getLogger(__name__)

class ServiceAlertas:
    """Serviço para gerenciamento de alertas de estoque"""
    
    def __init__(self):
        self.config_default = {
            "dias_vencimento_critico": 3,
            "dias_vencimento_atencao": 7,
            "dias_vencimento_aviso": 30,
            "ativar_alertas_email": False,
            "ativar_alertas_push": True
        }
    
    def verificar_todos_alertas(self, db: Session) -> List[AlertaSchema]:
        """Verifica e gera todos os tipos de alertas do sistema"""
        logger.info("Iniciando verificação completa de alertas")
        
        alertas = []
        
        # 1. Alertas de estoque crítico/baixo
        alertas.extend(self._verificar_alertas_estoque(db))
        
        # 2. Alertas de vencimento
        alertas.extend(self._verificar_alertas_vencimento(db))
        
        # 3. Salvar novos alertas no banco
        self._salvar_alertas(db, alertas)
        
        logger.info(f"Verificação concluída. {len(alertas)} alertas encontrados")
        return alertas
    
    def _verificar_alertas_estoque(self, db: Session) -> List[AlertaSchema]:
        """Verifica alertas relacionados a quantidade em estoque"""
        alertas = []
        
        # Query para buscar itens com estoque baixo/crítico
        query = db.query(
            ItemArmazenado,
            ItemEstoque,
            Armazem,
            case(
                (ItemEstoque.produto_medicamento_id.isnot(None), 
                 db.query(Medicamento.nome).filter(Medicamento.id == ItemEstoque.produto_medicamento_id).scalar_subquery()),
                (ItemEstoque.produto_cuidado_pessoal_id.isnot(None), 
                 db.query(CuidadoPessoal.nome).filter(CuidadoPessoal.id == ItemEstoque.produto_cuidado_pessoal_id).scalar_subquery()),
                (ItemEstoque.produto_suplemento_alimentar_id.isnot(None), 
                 db.query(SuplementoAlimentar.nome).filter(SuplementoAlimentar.id == ItemEstoque.produto_suplemento_alimentar_id).scalar_subquery()),
                else_="Produto Desconhecido"
            ).label('produto_nome')
        ).join(
            ItemEstoque, ItemArmazenado.item_estoque_id == ItemEstoque.id
        ).join(
            Armazem, ItemArmazenado.armazem_id == Armazem.id
        ).filter(
            ItemArmazenado.quantidade <= Armazem.quantidade_minima
        ).all()
        
        for item_armazenado, item_estoque, armazem, produto_nome in query:
            # Determinar tipo e prioridade
            if item_armazenado.quantidade == 0:
                tipo = TipoAlerta.FALTA_PRODUTO
                prioridade = PrioridadeAlerta.CRITICA
                titulo = f"FALTA TOTAL: {produto_nome}"
                descricao = f"Produto {produto_nome} está em falta total no {armazem.local_armazem}"
            elif item_armazenado.quantidade <= (armazem.quantidade_minima * 0.5):
                tipo = TipoAlerta.ESTOQUE_CRITICO
                prioridade = PrioridadeAlerta.ALTA
                titulo = f"ESTOQUE CRÍTICO: {produto_nome}"
                descricao = f"Produto {produto_nome} com apenas {item_armazenado.quantidade} unidades (mínimo: {armazem.quantidade_minima})"
            else:
                tipo = TipoAlerta.ESTOQUE_BAIXO
                prioridade = PrioridadeAlerta.MEDIA
                titulo = f"Estoque Baixo: {produto_nome}"
                descricao = f"Produto {produto_nome} abaixo do estoque mínimo ({item_armazenado.quantidade}/{armazem.quantidade_minima})"
            
            valor_total = item_armazenado.quantidade * item_estoque.preco
            
            alerta = AlertaSchema(
                tipo=tipo,
                prioridade=prioridade,
                titulo=titulo,
                descricao=descricao,
                item_estoque_id=item_estoque.id,
                produto_nome=produto_nome,
                codigo_barras=item_estoque.codigo_barras,
                armazem_id=armazem.id,
                armazem_nome=armazem.local_armazem,
                quantidade_atual=item_armazenado.quantidade,
                quantidade_minima=armazem.quantidade_minima,
                data_validade=item_estoque.data_validade,
                valor_unitario=item_estoque.preco,
                valor_total_impactado=valor_total
            )
            alertas.append(alerta)
        
        return alertas
    
    def _verificar_alertas_vencimento(self, db: Session) -> List[AlertaSchema]:
        """Verifica alertas relacionados a vencimento de produtos"""
        alertas = []
        hoje = datetime.now().date()
        
        # Buscar configurações de dias
        config = self._obter_configuracoes(db)
        dias_critico = config.get("dias_vencimento_critico", 3)
        dias_atencao = config.get("dias_vencimento_atencao", 7)
        dias_aviso = config.get("dias_vencimento_aviso", 30)
        
        # Query para produtos próximos ao vencimento
        limite_aviso = hoje + timedelta(days=dias_aviso)
        
        query = db.query(
            ItemArmazenado,
            ItemEstoque,
            Armazem,
            case(
                (ItemEstoque.produto_medicamento_id.isnot(None), 
                 db.query(Medicamento.nome).filter(Medicamento.id == ItemEstoque.produto_medicamento_id).scalar_subquery()),
                (ItemEstoque.produto_cuidado_pessoal_id.isnot(None), 
                 db.query(CuidadoPessoal.nome).filter(CuidadoPessoal.id == ItemEstoque.produto_cuidado_pessoal_id).scalar_subquery()),
                (ItemEstoque.produto_suplemento_alimentar_id.isnot(None), 
                 db.query(SuplementoAlimentar.nome).filter(SuplementoAlimentar.id == ItemEstoque.produto_suplemento_alimentar_id).scalar_subquery()),
                else_="Produto Desconhecido"
            ).label('produto_nome')
        ).join(
            ItemEstoque, ItemArmazenado.item_estoque_id == ItemEstoque.id
        ).join(
            Armazem, ItemArmazenado.armazem_id == Armazem.id
        ).filter(
            ItemEstoque.data_validade.cast(date) <= limite_aviso,
            ItemArmazenado.quantidade > 0  # Só alertar se tem estoque
        ).all()
        
        for item_armazenado, item_estoque, armazem, produto_nome in query:
            data_vencimento = item_estoque.data_validade.date() if item_estoque.data_validade else hoje
            dias_para_vencer = (data_vencimento - hoje).days
            
            # Determinar tipo e prioridade baseado nos dias
            if dias_para_vencer < 0:
                tipo = TipoAlerta.PRODUTO_VENCIDO
                prioridade = PrioridadeAlerta.CRITICA
                titulo = f"VENCIDO: {produto_nome}"
                descricao = f"Produto {produto_nome} venceu há {abs(dias_para_vencer)} dias"
            elif dias_para_vencer <= dias_critico:
                tipo = TipoAlerta.PROXIMO_VENCIMENTO
                prioridade = PrioridadeAlerta.CRITICA
                titulo = f"VENCE EM {dias_para_vencer} DIAS: {produto_nome}"
                descricao = f"Produto {produto_nome} vence em {dias_para_vencer} dias - ação urgente necessária"
            elif dias_para_vencer <= dias_atencao:
                tipo = TipoAlerta.PROXIMO_VENCIMENTO
                prioridade = PrioridadeAlerta.ALTA
                titulo = f"Vence em {dias_para_vencer} dias: {produto_nome}"
                descricao = f"Produto {produto_nome} vence em {dias_para_vencer} dias"
            else:
                tipo = TipoAlerta.PROXIMO_VENCIMENTO
                prioridade = PrioridadeAlerta.MEDIA
                titulo = f"Atenção vencimento: {produto_nome}"
                descricao = f"Produto {produto_nome} vence em {dias_para_vencer} dias"
            
            valor_total = item_armazenado.quantidade * item_estoque.preco
            
            alerta = AlertaSchema(
                tipo=tipo,
                prioridade=prioridade,
                titulo=titulo,
                descricao=descricao,
                item_estoque_id=item_estoque.id,
                produto_nome=produto_nome,
                codigo_barras=item_estoque.codigo_barras,
                armazem_id=armazem.id,
                armazem_nome=armazem.local_armazem,
                quantidade_atual=item_armazenado.quantidade,
                quantidade_minima=armazem.quantidade_minima,
                data_validade=item_estoque.data_validade,
                dias_para_vencimento=dias_para_vencer,
                valor_unitario=item_estoque.preco,
                valor_total_impactado=valor_total
            )
            alertas.append(alerta)
        
        return alertas
    
    def _salvar_alertas(self, db: Session, alertas: List[AlertaSchema]):
        """Salva novos alertas no banco de dados"""
        for alerta in alertas:
            # Verificar se já existe alerta similar não resolvido
            alerta_existente = db.query(AlertaEstoque).filter(
                and_(
                    AlertaEstoque.tipo == alerta.tipo.value,
                    AlertaEstoque.item_estoque_id == alerta.item_estoque_id,
                    AlertaEstoque.armazem_id == alerta.armazem_id,
                    AlertaEstoque.resolvido == False
                )
            ).first()
            
            if not alerta_existente:
                # Criar novo alerta
                novo_alerta = AlertaEstoque(
                    tipo=alerta.tipo.value,
                    prioridade=alerta.prioridade.value,
                    titulo=alerta.titulo,
                    descricao=alerta.descricao,
                    item_estoque_id=alerta.item_estoque_id,
                    armazem_id=alerta.armazem_id,
                    quantidade_atual=alerta.quantidade_atual,
                    quantidade_minima=alerta.quantidade_minima,
                    valor_unitario=alerta.valor_unitario,
                    valor_total_impactado=alerta.valor_total_impactado,
                    dias_para_vencimento=alerta.dias_para_vencimento
                )
                db.add(novo_alerta)
        
        db.commit()
    
    def obter_alertas(self, db: Session, filtros: FiltroAlertas) -> List[AlertaSchema]:
        """Obtém alertas com filtros aplicados"""
        query = db.query(
            AlertaEstoque,
            case(
                (ItemEstoque.produto_medicamento_id.isnot(None), 
                 db.query(Medicamento.nome).filter(Medicamento.id == ItemEstoque.produto_medicamento_id).scalar_subquery()),
                (ItemEstoque.produto_cuidado_pessoal_id.isnot(None), 
                 db.query(CuidadoPessoal.nome).filter(CuidadoPessoal.id == ItemEstoque.produto_cuidado_pessoal_id).scalar_subquery()),
                (ItemEstoque.produto_suplemento_alimentar_id.isnot(None), 
                 db.query(SuplementoAlimentar.nome).filter(SuplementoAlimentar.id == ItemEstoque.produto_suplemento_alimentar_id).scalar_subquery()),
                else_="Produto Desconhecido"
            ).label('produto_nome'),
            ItemEstoque.codigo_barras,
            Armazem.local_armazem
        ).join(
            ItemEstoque, AlertaEstoque.item_estoque_id == ItemEstoque.id
        ).join(
            Armazem, AlertaEstoque.armazem_id == Armazem.id
        )
        
        # Aplicar filtros
        if filtros.tipo:
            query = query.filter(AlertaEstoque.tipo == filtros.tipo.value)
        
        if filtros.prioridade:
            query = query.filter(AlertaEstoque.prioridade == filtros.prioridade.value)
        
        if filtros.armazem_id:
            query = query.filter(AlertaEstoque.armazem_id == filtros.armazem_id)
        
        if filtros.apenas_nao_resolvidos:
            query = query.filter(AlertaEstoque.resolvido == False)
        
        if filtros.dias_vencimento_max is not None:
            query = query.filter(
                or_(
                    AlertaEstoque.dias_para_vencimento.is_(None),
                    AlertaEstoque.dias_para_vencimento <= filtros.dias_vencimento_max
                )
            )
        
        # Ordenar por prioridade e data
        ordem_prioridade = case(
            (AlertaEstoque.prioridade == 'critica', 1),
            (AlertaEstoque.prioridade == 'alta', 2),
            (AlertaEstoque.prioridade == 'media', 3),
            (AlertaEstoque.prioridade == 'baixa', 4),
            else_=5
        )
        query = query.order_by(ordem_prioridade, AlertaEstoque.data_criacao.desc())
        
        resultados = query.all()
        
        # Converter para schema
        alertas = []
        for alerta_db, produto_nome, codigo_barras, armazem_nome in resultados:
            alerta = AlertaSchema(
                id=alerta_db.id,
                tipo=TipoAlerta(alerta_db.tipo),
                prioridade=PrioridadeAlerta(alerta_db.prioridade),
                titulo=alerta_db.titulo,
                descricao=alerta_db.descricao,
                item_estoque_id=alerta_db.item_estoque_id,
                produto_nome=produto_nome,
                codigo_barras=codigo_barras,
                armazem_id=alerta_db.armazem_id,
                armazem_nome=armazem_nome,
                quantidade_atual=alerta_db.quantidade_atual,
                quantidade_minima=alerta_db.quantidade_minima,
                data_validade=alerta_db.item_estoque.data_validade if alerta_db.item_estoque else None,
                dias_para_vencimento=alerta_db.dias_para_vencimento,
                valor_unitario=alerta_db.valor_unitario,
                valor_total_impactado=alerta_db.valor_total_impactado,
                data_criacao=alerta_db.data_criacao,
                data_resolucao=alerta_db.data_resolucao,
                resolvido=alerta_db.resolvido,
                observacoes=alerta_db.observacoes
            )
            alertas.append(alerta)
        
        return alertas
    
    def gerar_resumo_alertas(self, db: Session) -> ResumoAlertas:
        """Gera resumo estatístico dos alertas"""
        # Contar alertas por prioridade
        contadores = db.query(
            AlertaEstoque.prioridade,
            func.count(AlertaEstoque.id)
        ).filter(
            AlertaEstoque.resolvido == False
        ).group_by(AlertaEstoque.prioridade).all()
        
        stats = {prioridade: count for prioridade, count in contadores}
        
        # Contadores específicos
        produtos_falta = db.query(func.count(AlertaEstoque.id)).filter(
            and_(
                AlertaEstoque.tipo == TipoAlerta.FALTA_PRODUTO.value,
                AlertaEstoque.resolvido == False
            )
        ).scalar() or 0
        
        produtos_vencidos = db.query(func.count(AlertaEstoque.id)).filter(
            and_(
                AlertaEstoque.tipo == TipoAlerta.PRODUTO_VENCIDO.value,
                AlertaEstoque.resolvido == False
            )
        ).scalar() or 0
        
        produtos_vencendo_hoje = db.query(func.count(AlertaEstoque.id)).filter(
            and_(
                AlertaEstoque.tipo == TipoAlerta.PROXIMO_VENCIMENTO.value,
                AlertaEstoque.dias_para_vencimento == 0,
                AlertaEstoque.resolvido == False
            )
        ).scalar() or 0
        
        produtos_vencendo_3_dias = db.query(func.count(AlertaEstoque.id)).filter(
            and_(
                AlertaEstoque.tipo == TipoAlerta.PROXIMO_VENCIMENTO.value,
                AlertaEstoque.dias_para_vencimento <= 3,
                AlertaEstoque.resolvido == False
            )
        ).scalar() or 0
        
        # Valor total impactado
        valor_total = db.query(func.sum(AlertaEstoque.valor_total_impactado)).filter(
            AlertaEstoque.resolvido == False
        ).scalar() or 0.0
        
        total_alertas = sum(stats.values())
        
        return ResumoAlertas(
            total_alertas=total_alertas,
            alertas_criticos=stats.get('critica', 0),
            alertas_altos=stats.get('alta', 0),
            alertas_medios=stats.get('media', 0),
            alertas_baixos=stats.get('baixa', 0),
            produtos_em_falta=produtos_falta,
            produtos_vencidos=produtos_vencidos,
            produtos_vencendo_hoje=produtos_vencendo_hoje,
            produtos_vencendo_3_dias=produtos_vencendo_3_dias,
            valor_total_impactado=valor_total,
            ultima_atualizacao=datetime.now()
        )
    
    def obter_alertas_criticos(self, db: Session, limite: int = 10) -> List[AlertaCritico]:
        """Obtém os alertas mais críticos para dashboard"""
        alertas = self.obter_alertas(db, FiltroAlertas(
            prioridade=PrioridadeAlerta.CRITICA,
            apenas_nao_resolvidos=True
        ))
        
        # Converter para formato crítico simplificado
        alertas_criticos = []
        for alerta in alertas[:limite]:
            alertas_criticos.append(AlertaCritico(
                tipo=alerta.tipo,
                prioridade=alerta.prioridade,
                produto_nome=alerta.produto_nome,
                armazem_nome=alerta.armazem_nome,
                quantidade_atual=alerta.quantidade_atual,
                quantidade_minima=alerta.quantidade_minima,
                valor_impacto=alerta.valor_total_impactado,
                urgencia_dias=alerta.dias_para_vencimento
            ))
        
        return alertas_criticos
    
    def resolver_alerta(self, db: Session, alerta_id: int, observacoes: Optional[str] = None) -> bool:
        """Marca um alerta como resolvido"""
        alerta = db.query(AlertaEstoque).filter(AlertaEstoque.id == alerta_id).first()
        if not alerta:
            return False
        
        alerta.resolvido = True
        alerta.data_resolucao = datetime.now()
        if observacoes:
            alerta.observacoes = observacoes
        
        db.commit()
        return True
    
    def _obter_configuracoes(self, db: Session) -> dict:
        """Obtém configurações do sistema de alertas"""
        configs = db.query(ConfiguracaoAlertas).all()
        config_dict = {config.chave: config.valor for config in configs}
        
        # Aplicar valores padrão se não existirem
        for chave, valor in self.config_default.items():
            if chave not in config_dict:
                config_dict[chave] = valor
        
        # Converter strings para tipos apropriados
        for chave in ["dias_vencimento_critico", "dias_vencimento_atencao", "dias_vencimento_aviso"]:
            if chave in config_dict:
                config_dict[chave] = int(config_dict[chave])
        
        for chave in ["ativar_alertas_email", "ativar_alertas_push"]:
            if chave in config_dict:
                config_dict[chave] = config_dict[chave].lower() == 'true'
        
        return config_dict

# Instância global do serviço
service_alertas = ServiceAlertas()
