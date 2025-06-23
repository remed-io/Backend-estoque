from sqlalchemy import Column, Integer, String
from app.settings import Base

class RestricaoAlimentar(Base):
    __tablename__ = "restricao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), unique=True, nullable=False)

    def __str__(self):
        return self.nome