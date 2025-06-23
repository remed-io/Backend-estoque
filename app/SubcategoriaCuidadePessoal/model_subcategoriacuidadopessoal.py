from sqlalchemy import Column, Integer, String
from app.settings import Base

class SubcategoriaCuidadePessoal(Base):
    __tablename__ = "subcategoria_cuidadopessoal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=False)
