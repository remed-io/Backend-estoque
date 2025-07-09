from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, text
from typing import List, Optional
from datetime import datetime, date, timedelta
import hashlib

from app.ItemArmazenado.model_item_armazenado import ItemArmazenado
from app.ItemEstoque.model_item_estoque import ItemEstoque
from app.Medicamento.model_medicamento import Medicamento
from app.CuidadoPessoal.model_cuidado_pessoal import CuidadoPessoal
from app.SuplementoAlimentar.model_suplemento_alimentar import SuplementoAlimentar
from app.Armazem.model_armazem import Armazem

from .schema_alertas_estoque import (
    AlertaEstoque,
    FiltroAlertas,
    ResumoAlertas,
    ConfiguracaoAlertas,
    RelatorioAlertas,
    TipoAlerta,
    SeveridadeAlerta
)

class ServiceAlertasEstoque:
    
    @staticmethod
    def gerar_alertas(
        db: Session, 
        configuracao: Optional[ConfiguracaoAlertas] = None,
        filtros: Optional[FiltroAlertas] = None
    ) -> RelatorioAlertas:
        """
        Gera relatório completo de alertas de estoque crítico
        """
        
        if not configuracao:
            configuracao = ConfiguracaoAlertas()
        
        if not filtros:
            filtros = FiltroAlertas()
        
        alertas = []
        
        # 1. Alertas de estoque crítico/zero
        alertas_estoque = ServiceAlertasEstoque._gerar_alertas_estoque_critico(
            db, configuracao, filtros
        )
        alertas.extend(alertas_estoque)
        
        # 2. Alertas de vencimento
        alertas_vencimento = ServiceAlertasEstoque._gerar_alertas_vencimento(
            db, configuracao, filtros
        )
        alertas.extend(alertas_vencimento)
        
        # 3. Aplicar filtros adicionais
        alertas = ServiceAlertasEstoque._aplicar_filtros(alertas, filtros)
        
        # 4. Calcular resumo
        resumo = ServiceAlertasEstoque._calcular_resumo(alertas)
        
        return RelatorioAlertas(
            alertas=alertas,
            resumo=resumo,
            configuracao=configuracao,
            data_geracao=date.today()
        )
    
    @staticmethod
    def _gerar_alertas_estoque_critico(
        db: Session,
        configuracao: ConfiguracaoAlertas,
        filtros: FiltroAlertas
    ) -> List[AlertaEstoque]:
        """
        Gera alertas de estoque crítico baseado na quantidade mínima
        """
        alertas = []
        
        # Query para itens armazenados com quantidade <= quantidade_minima
        query = db.query(ItemArmazenado).options(
            joinedload(ItemArmazenado.item).joinedload(ItemEstoque.medicamento),
            joinedload(ItemArmazenado.item).joinedload(ItemEstoque.cuidado_pessoal),
            joinedload(ItemArmazenado.item).joinedload(ItemEstoque.suplemento_alimentar),
            joinedload(ItemArmazenado.armazem)
        )
        
        # Filtrar por armazém se especificado
        if filtros.armazem_id:
            query = query.filter(ItemArmazenado.armazem_id == filtros.armazem_id)
        
        # Buscar apenas itens com estoque crítico ou zero
        query = query.filter(
            ItemArmazenado.quantidade <= ItemArmazenado.armazem.has(
                Armazem.quantidade_minima
            )
        )
        
        items_criticos = query.all()
        
        for item_armazenado in items_criticos:
            # Determinar nome do produto
            produto_nome, categoria = ServiceAlertasEstoque._obter_dados_produto(
                item_armazenado.item
            )
            
            # Filtrar por nome do produto se especificado
            if filtros.produto_nome and filtros.produto_nome.lower() not in produto_nome.lower():
                continue
            
            # Determinar tipo e severidade do alerta
            if item_armazenado.quantidade == 0:
                tipo = TipoAlerta.estoque_zero
                severidade = configuracao.severidade_estoque_zero
                titulo = f"Estoque ZERADO: {produto_nome}"
                descricao = f"O produto {produto_nome} está com estoque zerado no armazém {item_armazenado.armazem.nome}"
            else:
                tipo = TipoAlerta.estoque_critico
                severidade = configuracao.severidade_estoque_critico
                titulo = f"Estoque CRÍTICO: {produto_nome}"
                descricao = f"O produto {produto_nome} está com estoque crítico ({item_armazenado.quantidade} unidades) no armazém {item_armazenado.armazem.nome}"
            
            # Gerar ID único para o alerta
            alerta_id = ServiceAlertasEstoque._gerar_id_alerta(
                tipo, item_armazenado.item_id, item_armazenado.armazem_id
            )
            
            alerta = AlertaEstoque(
                id=alerta_id,
                tipo=tipo,
                severidade=severidade,
                titulo=titulo,
                descricao=descricao,
                data_alerta=date.today(),
                produto_nome=produto_nome,
                categoria=categoria,
                armazem_id=item_armazenado.armazem_id,
                armazem_nome=item_armazenado.armazem.nome,
                quantidade_atual=item_armazenado.quantidade,
                quantidade_minima=item_armazenado.armazem.quantidade_minima
            )
            
            alertas.append(alerta)
        
        return alertas
    
    @staticmethod
    def _gerar_alertas_vencimento(
        db: Session,
        configuracao: ConfiguracaoAlertas,
        filtros: FiltroAlertas
    ) -> List[AlertaEstoque]:
        """
        Gera alertas de produtos vencidos ou próximos ao vencimento
        """
        alertas = []
        
        # Data limite para alertas de vencimento
        data_limite = date.today() + timedelta(days=configuracao.dias_aviso_vencimento)
        
        # Query para itens de estoque próximos ao vencimento
        query = db.query(ItemEstoque).options(
            joinedload(ItemEstoque.medicamento),
            joinedload(ItemEstoque.cuidado_pessoal),
            joinedload(ItemEstoque.suplemento_alimentar)
        )
        
        # Filtrar por data de vencimento
        condicoes_vencimento = []
        
        if configuracao.incluir_vencidos:
            condicoes_vencimento.append(ItemEstoque.data_vencimento < date.today())
        
        condicoes_vencimento.append(
            and_(
                ItemEstoque.data_vencimento >= date.today(),
                ItemEstoque.data_vencimento <= data_limite
            )
        )
        
        query = query.filter(or_(*condicoes_vencimento))
        
        items_vencimento = query.all()
        
        for item in items_vencimento:
            # Determinar nome do produto
            produto_nome, categoria = ServiceAlertasEstoque._obter_dados_produto(item)
            
            # Filtrar por nome do produto se especificado
            if filtros.produto_nome and filtros.produto_nome.lower() not in produto_nome.lower():
                continue
            
            # Verificar se item está em algum armazém (através de ItemArmazenado)
            item_armazenado = db.query(ItemArmazenado).filter(
                ItemArmazenado.item_id == item.id
            ).first()
            
            if not item_armazenado:
                continue
            
            # Filtrar por armazém se especificado
            if filtros.armazem_id and item_armazenado.armazem_id != filtros.armazem_id:
                continue
            
            # Calcular dias para vencer
            dias_para_vencer = (item.data_vencimento - date.today()).days
            
            # Determinar tipo e severidade
            if dias_para_vencer < 0:
                tipo = TipoAlerta.produto_vencido
                severidade = SeveridadeAlerta.critica
                titulo = f"Produto VENCIDO: {produto_nome}"
                descricao = f"O produto {produto_nome} (lote {item.lote}) venceu há {abs(dias_para_vencer)} dias"
            else:
                tipo = TipoAlerta.produto_proximo_vencimento
                if dias_para_vencer <= 7:
                    severidade = SeveridadeAlerta.alta
                elif dias_para_vencer <= 15:
                    severidade = SeveridadeAlerta.media
                else:
                    severidade = SeveridadeAlerta.baixa
                
                titulo = f"Produto próximo ao vencimento: {produto_nome}"
                descricao = f"O produto {produto_nome} (lote {item.lote}) vence em {dias_para_vencer} dias"
            
            # Gerar ID único para o alerta
            alerta_id = ServiceAlertasEstoque._gerar_id_alerta(
                tipo, item.id, item_armazenado.armazem_id, item.lote
            )
            
            alerta = AlertaEstoque(
                id=alerta_id,
                tipo=tipo,
                severidade=severidade,
                titulo=titulo,
                descricao=descricao,
                data_alerta=date.today(),
                produto_nome=produto_nome,
                categoria=categoria,
                armazem_id=item_armazenado.armazem_id,
                armazem_nome=item_armazenado.armazem.nome,
                quantidade_atual=item_armazenado.quantidade,
                quantidade_minima=item_armazenado.armazem.quantidade_minima,
                item_id=item.id,
                lote=item.lote,
                data_vencimento=item.data_vencimento,
                dias_para_vencer=dias_para_vencer
            )
            
            alertas.append(alerta)
        
        return alertas
    
    @staticmethod
    def _obter_dados_produto(item_estoque: ItemEstoque) -> tuple[str, str]:
        """
        Obtém nome e categoria do produto baseado no item de estoque
        """
        if item_estoque.medicamento:
            return item_estoque.medicamento.nome, "Medicamento"
        elif item_estoque.cuidado_pessoal:
            return item_estoque.cuidado_pessoal.nome, "Cuidado Pessoal"
        elif item_estoque.suplemento_alimentar:
            return item_estoque.suplemento_alimentar.nome, "Suplemento Alimentar"
        else:
            return "Produto Desconhecido", "Desconhecido"
    
    @staticmethod
    def _gerar_id_alerta(tipo: TipoAlerta, item_id: int, armazem_id: int, lote: str = None) -> str:
        """
        Gera ID único para o alerta baseado nos dados
        """
        dados = f"{tipo.value}_{item_id}_{armazem_id}_{lote or ''}"
        return hashlib.md5(dados.encode()).hexdigest()[:12]
    
    @staticmethod
    def _aplicar_filtros(alertas: List[AlertaEstoque], filtros: FiltroAlertas) -> List[AlertaEstoque]:
        """
        Aplica filtros adicionais aos alertas
        """
        if filtros.tipos:
            alertas = [a for a in alertas if a.tipo in filtros.tipos]
        
        if filtros.severidades:
            alertas = [a for a in alertas if a.severidade in filtros.severidades]
        
        if filtros.apenas_criticos:
            alertas = [a for a in alertas if a.severidade in [SeveridadeAlerta.critica, SeveridadeAlerta.alta]]
        
        return alertas
    
    @staticmethod
    def _calcular_resumo(alertas: List[AlertaEstoque]) -> ResumoAlertas:
        """
        Calcula resumo dos alertas
        """
        total_alertas = len(alertas)
        
        # Por severidade
        criticos = len([a for a in alertas if a.severidade == SeveridadeAlerta.critica])
        altos = len([a for a in alertas if a.severidade == SeveridadeAlerta.alta])
        medios = len([a for a in alertas if a.severidade == SeveridadeAlerta.media])
        baixos = len([a for a in alertas if a.severidade == SeveridadeAlerta.baixa])
        
        # Por tipo
        estoque_critico = len([a for a in alertas if a.tipo == TipoAlerta.estoque_critico])
        estoque_zero = len([a for a in alertas if a.tipo == TipoAlerta.estoque_zero])
        vencidos = len([a for a in alertas if a.tipo == TipoAlerta.produto_vencido])
        proximo_vencimento = len([a for a in alertas if a.tipo == TipoAlerta.produto_proximo_vencimento])
        
        # Armazéns afetados
        armazens_unicos = set(a.armazem_id for a in alertas)
        
        return ResumoAlertas(
            total_alertas=total_alertas,
            alertas_criticos=criticos,
            alertas_altos=altos,
            alertas_medios=medios,
            alertas_baixos=baixos,
            estoque_critico=estoque_critico,
            estoque_zero=estoque_zero,
            produtos_vencidos=vencidos,
            produtos_proximo_vencimento=proximo_vencimento,
            armazens_afetados=len(armazens_unicos)
        )
    
    @staticmethod
    def obter_alertas_criticos(db: Session, armazem_id: Optional[int] = None) -> List[AlertaEstoque]:
        """
        Obtém apenas alertas críticos e de alta severidade
        """
        filtros = FiltroAlertas(
            apenas_criticos=True,
            armazem_id=armazem_id
        )
        
        relatorio = ServiceAlertasEstoque.gerar_alertas(db, filtros=filtros)
        return relatorio.alertas
    
    @staticmethod
    def obter_resumo_dashboard(db: Session) -> ResumoAlertas:
        """
        Obtém resumo rápido para dashboard
        """
        relatorio = ServiceAlertasEstoque.gerar_alertas(db)
        return relatorio.resumo
