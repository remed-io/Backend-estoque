from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.settings import Base

class ItemEstoque(Base):
    __tablename__ = "item_estoque"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_barras = Column(String(100), nullable=False, unique=True)
    produto_nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    validade = Column(DateTime, nullable=False)
    fornecedor_id = Column(Integer, ForeignKey('fornecedor.id'))

    fornecedor = relationship("Fornecedor")
