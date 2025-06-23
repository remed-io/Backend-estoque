#app/models/armazem.py

from sqlalchemy import Column, Integer, String
from app.settings import Base

class Armazem(Base):
    __tablename__ = "armazem"

    id = Column(Integer, primary_key=True, autoincrement=True)
    local_armazem = Column(String(100), nullable=False)
