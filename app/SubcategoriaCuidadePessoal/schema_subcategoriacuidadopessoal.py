from pydantic import BaseModel

class SubcategoriaCuidadePessoalBase(BaseModel):
    nome: str
    descricao: str

class SubcategoriaCuidadePessoalCreate(SubcategoriaCuidadePessoalBase):
    pass

class SubcategoriaCuidadePessoalRead(SubcategoriaCuidadePessoalBase):
    id: int

    class Config:
        orm_mode = True
