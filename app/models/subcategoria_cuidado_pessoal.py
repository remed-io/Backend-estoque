#app/models/subcategoria_cuidado_pessoal

from sqlalchemy import Column, Integer, String
from settings import Base
from sqlalchemy.orm import relationship

class SubcategoriaCuidadoPessoal(Base):
    __tablename__ = "subcategoriacuidadossoal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    descricao = Column(String(255))
    produtos = relationship("CuidadoPessoal", back_populates="subcategoria")