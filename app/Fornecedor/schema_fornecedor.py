from pydantic import BaseModel

class FornecedorBase(BaseModel):
    nome: str
    cnpj: str
    contato: str

class FornecedorCreate(FornecedorBase):
    pass

class FornecedorRead(FornecedorBase):
    id: int

    class Config:
        orm_mode = True
