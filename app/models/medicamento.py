#app/models/medicamento.py

from sqlalchemy import Column, Integer, String, Text
from settings import Base

class Medicamento(Base):
    __tablename__ = "medicamento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    principio_ativo = Column(String(100))
    tarja = Column(String(50))
    restricoes = Column(Text)
    fabricante = Column(String(100))
    registro_anvisa = Column(String(50))