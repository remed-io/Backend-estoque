from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.settings import Base

class MovimentacaoEstoque(Base):
    __tablename__ = "movimentacao_estoque"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(DateTime, nullable=False)
    tipo = Column(String(50), nullable=False)
    quantidade = Column(Integer, nullable=False)
    item_id = Column(Integer, ForeignKey('item_estoque.id'))
    responsavel_id = Column(Integer, ForeignKey('funcionario.id'))
    cpf_comprador = Column(String(20), nullable=True)
    nome_comprador = Column(String(100), nullable=True)
    receita_digital = Column(String(255), nullable=True)
    armazem_id = Column(Integer, ForeignKey('armazem.id'), nullable=False)

    item = relationship("ItemEstoque")
    responsavel = relationship("Funcionario")
    armazem = relationship("Armazem")
