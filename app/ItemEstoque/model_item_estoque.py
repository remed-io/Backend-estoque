from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.settings import Base

class ItemEstoque(Base):
    __tablename__ = "item_estoque"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_barras = Column(String(100), nullable=False, unique=True)
    preco = Column(Float, nullable=False)
    data_validade = Column(DateTime, nullable=False)
    fornecedor_id = Column(Integer, ForeignKey('fornecedor.id'))
    lote = Column(String(50), nullable=False)

    produto_medicamento_id = Column(Integer, ForeignKey('medicamento.id'), nullable=True)
    produto_cuidado_pessoal_id = Column(Integer, ForeignKey('cuidado_pessoal.id'), nullable=True)
    produto_suplemento_alimentar_id = Column(Integer, ForeignKey('suplemento_alimentar.id'), nullable=True)
    
    produto_id = Column(Integer, nullable=True)
    produto_nome = Column(String(100), nullable=True)
    tipo_produto = Column(String(30), nullable=False)


    fornecedor = relationship("Fornecedor")
    medicamento = relationship("Medicamento", back_populates="itens_estoque")
    cuidado_pessoal = relationship("CuidadoPessoal", back_populates="itens_estoque")
    suplemento_alimentar = relationship("SuplementoAlimentar", back_populates="itens_estoque")
