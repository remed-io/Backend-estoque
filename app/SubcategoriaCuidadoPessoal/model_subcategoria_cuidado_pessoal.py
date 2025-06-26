from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.settings import Base

class SubcategoriaCuidadoPessoal(Base):
    __tablename__ = "subcategoria_cuidado_pessoal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=False)
    produtos = relationship("CuidadoPessoal", back_populates="subcategoria")
