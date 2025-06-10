#app/models/fornecedor.py

from sqlalchemy import Column, Integer, String
from settings import Base

class Fornecedor(Base):
    __tablename__ = "fornecedor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cnpj = Column(String(20), nullable=False, unique=True)
    contato = Column(String(100))