from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.settings import Base
from datetime import datetime

class AlertaEstoque(Base):
    """Modelo para alertas de estoque"""
    __tablename__ = "alerta_estoque"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(50), nullable=False)  # estoque_critico, estoque_baixo, produto_vencido, etc.
    prioridade = Column(String(20), nullable=False)  # baixa, media, alta, critica
    titulo = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=False)
    
    # Referências
    item_estoque_id = Column(Integer, ForeignKey('item_estoque.id'), nullable=False)
    armazem_id = Column(Integer, ForeignKey('armazem.id'), nullable=False)
    
    # Dados do contexto
    quantidade_atual = Column(Integer, nullable=False)
    quantidade_minima = Column(Integer, nullable=False)
    valor_unitario = Column(Float, nullable=False)
    valor_total_impactado = Column(Float, nullable=False)
    dias_para_vencimento = Column(Integer, nullable=True)
    
    # Controle
    data_criacao = Column(DateTime, nullable=False, default=datetime.now)
    data_resolucao = Column(DateTime, nullable=True)
    resolvido = Column(Boolean, nullable=False, default=False)
    observacoes = Column(Text, nullable=True)
    
    # Relacionamentos
    item_estoque = relationship("ItemEstoque")
    armazem = relationship("Armazem")

class NotificacaoAlerta(Base):
    """Modelo para notificações de alertas"""
    __tablename__ = "notificacao_alerta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    alerta_id = Column(Integer, ForeignKey('alerta_estoque.id'), nullable=False)
    funcionario_id = Column(Integer, ForeignKey('funcionario.id'), nullable=True)
    tipo_notificacao = Column(String(20), nullable=False)  # email, push, sms
    enviado = Column(Boolean, nullable=False, default=False)
    data_envio = Column(DateTime, nullable=True)
    tentativas_envio = Column(Integer, nullable=False, default=0)
    erro_envio = Column(Text, nullable=True)
    
    # Relacionamentos
    alerta = relationship("AlertaEstoque")
    funcionario = relationship("Funcionario")

class ConfiguracaoAlertas(Base):
    """Configurações globais do sistema de alertas"""
    __tablename__ = "configuracao_alertas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chave = Column(String(100), nullable=False, unique=True)
    valor = Column(String(500), nullable=False)
    descricao = Column(Text, nullable=True)
    data_atualizacao = Column(DateTime, nullable=False, default=datetime.now)
