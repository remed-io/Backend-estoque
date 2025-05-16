from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.produto_schema import ProdutoCreate, ProdutoOut
from app.services import produto_service
from app.database import get_session
from typing import List

router = APIRouter()

@router.post("/", response_model=ProdutoOut)
async def criar(produto: ProdutoCreate, session: AsyncSession = Depends(get_session)):
    return await produto_service.criar_produto(session, produto)

@router.get("/", response_model=List[ProdutoOut])
async def listar(session: AsyncSession = Depends(get_session)):
    return await produto_service.listar_produtos(session)
