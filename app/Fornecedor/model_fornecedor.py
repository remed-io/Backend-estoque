from sqlalchemy import Column, Integer, String
from app.settings import Base

class Fornecedor(Base):
    __tablename__ = "fornecedor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cnpj = Column(String(30), nullable=False, unique=True)
    contato = Column(String(100), nullable=False)

    def __str__(self):
        return self.nome
