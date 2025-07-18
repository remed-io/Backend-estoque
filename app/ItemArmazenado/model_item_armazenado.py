from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, UniqueConstraint
from app.settings import Base

class ItemArmazenado(Base):
    __tablename__ = 'item_armazenado'
    id = Column(Integer, primary_key=True, index=True)
    armazem_id = Column(Integer, ForeignKey('armazem.id'), nullable=False)
    item_estoque_id = Column(Integer, ForeignKey('item_estoque.id'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data_atualizacao = Column(TIMESTAMP, nullable=False)
    __table_args__ = (UniqueConstraint('armazem_id', 'item_estoque_id', name='uix_armazem_item'),) 