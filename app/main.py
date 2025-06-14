
import os

from fastapi import FastAPI
from sqlalchemy import create_engine, text  # Adicione text aqui
from sqlalchemy.orm import sessionmaker
from app.routes import (armazenamento_routes , fornecedor_routes , restricao_routes ,
                        funcionario_routes)

from fastapi import FastAPI

app = FastAPI()

app.include_router(armazenamento_routes.router)
app.include_router(fornecedor_routes.router)
app.include_router(restricao_routes.router)
app.include_router(funcionario_routes.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

