from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.MovimentacaoEstoque.model_movimentacao_estoque import MovimentacaoEstoque
from app.MovimentacaoEstoque.schema_movimentacao_estoque import MovimentacaoEstoqueCreate

def create_movimentacaoestoque(db: Session, movimentacao: MovimentacaoEstoqueCreate):
    db_movimentacao = MovimentacaoEstoque(**movimentacao.dict())
    db.add(db_movimentacao)
    db.commit()
    db.refresh(db_movimentacao)
    return db_movimentacao

def get_all_movimentacoes(db: Session):
    return db.query(MovimentacaoEstoque).all()

def get_movimentacao_by_id(db: Session, id: int):
    return db.query(MovimentacaoEstoque).filter(MovimentacaoEstoque.id == id).first()

def update_movimentacao(db: Session, id: int, movimentacao: MovimentacaoEstoqueCreate):
    db_movimentacao = db.query(MovimentacaoEstoque).filter(MovimentacaoEstoque.id == id).first()
    if not db_movimentacao:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    for key, value in movimentacao.dict().items():
        setattr(db_movimentacao, key, value)
    db.commit()
    db.refresh(db_movimentacao)
    return db_movimentacao

def delete_movimentacao(db: Session, id: int):
    db_movimentacao = db.query(MovimentacaoEstoque).filter(MovimentacaoEstoque.id == id).first()
    if not db_movimentacao:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    db.delete(db_movimentacao)
    db.commit()
    return {"message": "Movimentação deletada com sucesso"}
