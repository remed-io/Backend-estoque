from sqlalchemy import Column, Integer, String, Text
from settings import Base

class SuplementoAlimentar(Base):
    __tablename__ = "suplemento_alimentar"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    principio_ativo = Column(String(100))
    restricoes = Column(Text)
    fabricante = Column(String(100))
    registro_anvisa = Column(String(50))