
import os

from fastapi import FastAPI
from sqlalchemy import create_engine, text  # Adicione text aqui
from sqlalchemy.orm import sessionmaker

from app.Armazem.routes_armazem import router as router_armazem
# from app.CuidadoPessoal import router_cuidado_pessoal
from app.Farmacia.routes_farmacia import router as router_farmacia
from app.Fornecedor.routes_fornecedor import router as router_fornecedor
from app.Funcionario.routes_funcionario import router as router_funcionario
from app.ItemEstoque.routes_item_estoque import router as router_item_estoque
# from app.Medicamento import router as router_medicamento
from app.MovimentacaoEstoque.routes_movimentacao_estoque import router as router_movimentacao_estoque
from app.RestricaoAlimentar.routes_restricao_alimentar import router as router_restricao_alimentar
from app.SubcategoriaCuidadoPessoal.routes_subcategoria_cuidado_pessoal import router as router_subcategoria_cuidado_pessoal
# from app.SuplementoAlimentar import router as router_suplemento_alimentar


app = FastAPI()

app.include_router(router_armazem, prefix="/armazem", tags=["Armazém"])
# app.include_router(router_cuidado_pessoal, prefix="/cuidado-pessoal", tags=["Cuidado Pessoal"])
app.include_router(router_farmacia, prefix="/farmacia", tags=["Farmácia"])
app.include_router(router_fornecedor, prefix="/fornecedor", tags=["Fornecedor"])
app.include_router(router_funcionario, prefix="/funcionario", tags=["Funcionário"])
app.include_router(router_item_estoque, prefix="/item-estoque", tags=["Item Estoque"])
# app.include_router(router_medicamento, prefix="/medicamento", tags=["Medicamento"])
app.include_router(router_movimentacao_estoque, prefix="/movimentacao-estoque", tags=["Movimentação Estoque"])
app.include_router(router_restricao_alimentar, prefix="/restricao-alimentar", tags=["Restrição Alimentar"])
app.include_router(router_subcategoria_cuidado_pessoal, prefix="/subcategoria-cuidado-pessoal", tags=["Subcategoria Cuidado Pessoal"])
# app.include_router(router_suplemento_alimentar, prefix="/suplemento-alimentar", tags=["Suplemento Alimentar"])  


@app.get("/")
async def root():
    return {"message": "Hello World"}

