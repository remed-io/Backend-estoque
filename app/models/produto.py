from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    validade = Column(DateTime)
    # Remova a coluna e relacionamento com fornecedor
