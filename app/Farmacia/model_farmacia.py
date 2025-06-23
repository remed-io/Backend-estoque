from sqlalchemy import Column, Integer, String
from app.settings import Base

class Farmacia(Base):
    __tablename__ = "farmacia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Relacionamentos serão definidos posteriormente
