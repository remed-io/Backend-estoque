# app/models/funcionario.py
from sqlalchemy import Column, Integer, String, DateTime
from app.settings import Base
from datetime import datetime

class Funcionario(Base):
    __tablename__ = "funcionario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)
    cargo = Column(String(50), nullable=False)
    data_contratacao = Column(DateTime, nullable=False, default=datetime.utcnow)