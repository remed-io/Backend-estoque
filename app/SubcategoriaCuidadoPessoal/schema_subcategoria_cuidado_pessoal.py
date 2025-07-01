from pydantic import BaseModel

class SubcategoriaCuidadoPessoalBase(BaseModel):
    nome: str
    descricao: str

class SubcategoriaCuidadoPessoalCreate(SubcategoriaCuidadoPessoalBase):
    pass

class SubcategoriaCuidadoPessoalRead(SubcategoriaCuidadoPessoalBase):
    id: int

    class Config:
        from_attributes = True
