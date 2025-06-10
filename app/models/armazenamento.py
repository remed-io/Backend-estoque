#app/models/armazenamento.py

from sqlalchemy import Column, Integer, String
from settings import Base

class Armazenamento(Base):
    __tablename__ = "armazenamento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    local_armazenamento = Column(String(100), nullable=False)
