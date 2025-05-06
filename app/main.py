from fastapi import FastAPI
from app.routes import produto_routes

app = FastAPI()

# Rota principal
@app.get("/")
def read_root():
    return {"message": "Hello World da Farmácia!"}

# Incluir outras rotas
app.include_router(produto_routes.router, prefix="/produtos")
