from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.settings import Base

class Medicamento(Base):
    __tablename__ = "medicamento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    dosagem = Column(String(50))
    principio_ativo = Column(String(100))
    tarja = Column(String(50))
    necessita_receita = Column(Integer, nullable=False, default=0)  # BOOLEAN no banco, pode ser Integer 0/1
    forma_farmaceutica = Column(String(50))
    fabricante = Column(String(100))
    registro_anvisa = Column(String(50))
    
    itens_estoque = relationship("ItemEstoque", back_populates="produto_medicamento")
    
    def __str__(self):
        return self.nome