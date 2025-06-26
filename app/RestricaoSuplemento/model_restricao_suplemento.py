from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.settings import Base

class RestricaoSuplemento(Base):
    __tablename__ = 'restricao_suplemento'
    suplemento_alimentar_id = Column(Integer, ForeignKey('suplemento_alimentar.id'), primary_key=True)
    restricao_alimentar_id = Column(Integer, ForeignKey('restricao_alimentar.id'), primary_key=True)
    severidade = Column(String(20))
    observacoes = Column(Text) 