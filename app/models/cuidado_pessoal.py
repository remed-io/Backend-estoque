# app/models/cuidado_pessoal.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from settings import Base

class CuidadoPessoal(Base):
    __tablename__ = "cuidado_pessoal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    subcategoria_id = Column(Integer, ForeignKey("subcategoriacuidadossoal.id"))
    forma = Column(String(50))
    quantidade = Column(String(20))
    volume = Column(String(20))
    uso_recomendado = Column(String(100))
    publico_alvo = Column(String(50))
    fabricante = Column(String(100))

    subcategoria = relationship("SubcategoriaCuidadoPessoal", back_populates="produtos")