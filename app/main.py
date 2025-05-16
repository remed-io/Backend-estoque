from fastapi import FastAPI
from app.routes import produto_route

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(produto_route.router, prefix="/produtos", tags=["Produtos"])