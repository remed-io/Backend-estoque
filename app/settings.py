import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

USE_SQLITE_FOR_TESTS = os.getenv("USE_SQLITE_FOR_TESTS", "false").lower() == "true"

if USE_SQLITE_FOR_TESTS:
    print(" Usando banco de testes em SQLite (modo teste)")
    DATABASE_URL = "sqlite:///:memory:"
    connect_args = {"check_same_thread": False}
else:
    DATABASE_URL = os.getenv("DATABASE_URL")
    connect_args = {}

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não definida e fallback não ativado.")

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
