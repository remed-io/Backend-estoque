#app/models/armazem.py

from sqlalchemy import Column, Integer, String, UniqueConstraint
from app.settings import Base

class Armazem(Base):
    __tablename__ = "armazem"

    id = Column(Integer, primary_key=True, autoincrement=True)
    local_armazem = Column(String(100), nullable=False, unique=True)
    __table_args__ = (UniqueConstraint('local_armazem', name='uix_local_armazem'),)
    
    def __str__(self):
        return self.nome
