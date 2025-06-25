from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.settings import Base

class SuplementoAlimentar(Base):
    __tablename__ = "suplemento_alimentar"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    principio_ativo = Column(String(100))
    sabor = Column(String(50))
    peso_volume = Column(String(20))
    fabricante = Column(String(100))
    registro_anvisa = Column(String(50))

    itens_estoque = relationship("ItemEstoque", back_populates="produto_suplemento_alimentar")

    def __str__(self):
        return self.nome