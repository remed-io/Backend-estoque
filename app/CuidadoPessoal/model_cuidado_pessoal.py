from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.settings import Base

class CuidadoPessoal(Base):
    __tablename__ = "cuidado_pessoal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    subcategoria_id = Column(Integer, ForeignKey("subcategoria_cuidado_pessoal.id"))
    quantidade = Column(String(20))
    volume = Column(String(20))
    uso_recomendado = Column(String(100))
    publico_alvo = Column(String(50))
    fabricante = Column(String(100))

    subcategoria = relationship("SubcategoriaCuidadoPessoal", back_populates="produtos")
    itens_estoque = relationship("ItemEstoque", back_populates="produto_cuidado_pessoal")
    
    def __str__(self):
        return self.nome    