from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.Funcionario.model_funcionario import Funcionario
from app.Funcionario.schema_funcionario import FuncionarioCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_funcionario(db: Session, funcionario: FuncionarioCreate):
    # Verifica se CPF ou email já existem
    existing_cpf = db.query(Funcionario).filter(Funcionario.cpf == funcionario.cpf).first()
    existing_email = db.query(Funcionario).filter(Funcionario.email == funcionario.email).first()
    
    if existing_cpf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado"
        )
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    hashed_password = get_password_hash(funcionario.senha)
    db_funcionario = Funcionario(
        nome=funcionario.nome,
        cpf=funcionario.cpf,
        email=funcionario.email,
        senha_hash=hashed_password,
        cargo=funcionario.cargo
    )
    
    db.add(db_funcionario)
    db.commit()
    db.refresh(db_funcionario)
    return db_funcionario

def get_all_funcionarios(db: Session):
    return db.query(Funcionario).all()

def get_funcionario_by_id(db: Session, id: int):
    return db.query(Funcionario).filter(Funcionario.id == id).first()

def get_funcionario_by_email(db: Session, email: str):
    return db.query(Funcionario).filter(Funcionario.email == email).first()

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_funcionario(db: Session, email: str, password: str):
    funcionario = get_funcionario_by_email(db, email)
    if not funcionario:
        return None
    if not verify_password(password, funcionario.senha_hash):
        return None
    return funcionario

def update_funcionario(db: Session, id: int, funcionario: FuncionarioCreate):
    db_funcionario = db.query(Funcionario).filter(Funcionario.id == id).first()
    if not db_funcionario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )
    
    # Verifica se novos CPF ou email já existem
    if funcionario.cpf != db_funcionario.cpf:
        existing_cpf = db.query(Funcionario).filter(Funcionario.cpf == funcionario.cpf).first()
        if existing_cpf:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF já cadastrado para outro funcionário"
            )
    
    if funcionario.email != db_funcionario.email:
        existing_email = db.query(Funcionario).filter(Funcionario.email == funcionario.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado para outro funcionário"
            )
    
    # Atualiza os campos
    for field, value in funcionario.dict(exclude={"senha"}).items():
        setattr(db_funcionario, field, value)
    
    if funcionario.senha:
        db_funcionario.senha_hash = get_password_hash(funcionario.senha)
    
    db.commit()
    db.refresh(db_funcionario)
    return db_funcionario

def delete_funcionario(db: Session, id: int):
    db_funcionario = db.query(Funcionario).filter(Funcionario.id == id).first()
    if not db_funcionario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )
    db.delete(db_funcionario)
    db.commit()
    return {"message": "Funcionário removido com sucesso"}
