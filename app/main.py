import os

from fastapi import FastAPI
from sqlalchemy import create_engine, text  # Adicione text aqui
from sqlalchemy.orm import sessionmaker

from app.Armazem.routes_armazem import router as router_armazem
from app.CuidadoPessoal.routes_cuidado_pessoal import router as router_cuidado_pessoal
from app.Farmacia.routes_farmacia import router as router_farmacia
from app.Fornecedor.routes_fornecedor import router as router_fornecedor
from app.Funcionario.routes_funcionario import router as router_funcionario
from app.ItemEstoque.routes_item_estoque import router as router_item_estoque
from app.Medicamento.routes_medicamento import router as router_medicamento
from app.MovimentacaoEstoque.routes_movimentacao_estoque import router as router_movimentacao_estoque
from app.RestricaoAlimentar.routes_restricao_alimentar import router as router_restricao_alimentar
from app.SubcategoriaCuidadoPessoal.routes_subcategoria_cuidado_pessoal import router as router_subcategoria_cuidado_pessoal
from app.SuplementoAlimentar.routes_suplemento_alimentar import router as router_suplemento_alimentar
from app.ItemArmazenado.routes_item_armazenado import router as router_item_armazenado
from app.RestricaoSuplemento.routes_restricao_suplemento import router as router_restricao_suplemento


app = FastAPI()

app.include_router(router_armazem)
app.include_router(router_cuidado_pessoal)
app.include_router(router_farmacia)
app.include_router(router_fornecedor)
app.include_router(router_funcionario)
app.include_router(router_item_estoque)
app.include_router(router_medicamento)
app.include_router(router_movimentacao_estoque)
app.include_router(router_restricao_alimentar)
app.include_router(router_subcategoria_cuidado_pessoal)
app.include_router(router_suplemento_alimentar)
app.include_router(router_item_armazenado)
app.include_router(router_restricao_suplemento)  


@app.get("/")
async def root():
    return {"message": "Hello World"}

