from app.models.produto import Produto
from app.schemas.produto_schema import ProdutoCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def criar_produto(session: AsyncSession, produto: ProdutoCreate):
    novo_produto = Produto(**produto.dict()) 
    session.add(novo_produto)
    await session.commit()
    await session.refresh(novo_produto)
    return novo_produto

async def listar_produtos(session: AsyncSession):
    result = await session.execute(select(Produto))
    return result.scalars().all()
