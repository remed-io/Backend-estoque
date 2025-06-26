from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime

class FuncionarioBase(BaseModel):
    nome: str = Field(..., max_length=50)
    cpf: str = Field(..., min_length=11, max_length=11)
    email: EmailStr
    cargo: str = Field(..., max_length=50)

class FuncionarioCreate(FuncionarioBase):
    senha: str = Field(..., min_length=8)
    
    @validator('senha')
    def senha_forte(cls, v):
        if len(v) < 8:
            raise ValueError('A senha deve ter pelo menos 8 caracteres')
        return v

class FuncionarioRead(FuncionarioBase):
    id: int
    data_contratacao: datetime

    class Config:
        orm_mode = True

class FuncionarioLogin(BaseModel):
    email: EmailStr
    senha: str
