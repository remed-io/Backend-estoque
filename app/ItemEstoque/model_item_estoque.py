from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.settings import Base

class ItemEstoque(Base):
    __tablename__ = "item_estoque"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_barras = Column(String(100), nullable=False, unique=True)
    preco = Column(Float, nullable=False)
    validade = Column(DateTime, nullable=False)
    fornecedor_id = Column(Integer, ForeignKey('fornecedor.id'))
    produto_medicamento_id = Column(Integer, ForeignKey('medicamento.id' ), nullable=True)
    produto_cuidado_pessoal_id = Column(Integer, ForeignKey('cuidado_pessoal.id'), nullable=True)
    produto_suplemento_alimentar_id = Column(Integer, ForeignKey('suplemento_alimentar.id'), nullable=True) 
    
    fornecedor = relationship("Fornecedor")
    produto_medicamento = relationship("Medicamento", back_populates="itens_estoque")
    produto_cuidado_pessoal = relationship("CuidadoPessoal", back_populates="itens_estoque")
    produto_suplemento_alimentar = relationship("SuplementoAlimentar", back_populates="itens_estoque")  