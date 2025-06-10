#app/models/restricao.py
from sqlalchemy import Column, Integer, String
from settings import Base

class Restricao(Base):
    __tablename__ = "restricao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), unique=True, nullable=False)