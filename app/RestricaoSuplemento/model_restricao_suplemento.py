from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.settings import Base

class RestricaoSuplemento(Base):
    __tablename__ = 'RestricaoSuplemento'
    suplemento_alimentar_id = Column(Integer, ForeignKey('SuplementoAlimentar.id'), primary_key=True)
    restricao_alimentar_id = Column(Integer, ForeignKey('RestricaoAlimentar.id'), primary_key=True)
    severidade = Column(String(20))
    observacoes = Column(Text) 