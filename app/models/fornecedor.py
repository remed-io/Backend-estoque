from pydantic import BaseModel

class Fornecedor(BaseModel):
    """
    Classe que representa um fornecedor.
    Atributos:
        nome (str): Nome do fornecedor.
        cnpj (str): CNPJ do fornecedor.
        contato (str): Contato do fornecedor.
    """
    
    def __init__(self, nome: str, cnpj: str, contato: str):
        self.nome = nome
        self.cnpj = cnpj
        self.contato = contato

    def __str__(self):
        return (
            f"Fornecedor(nome={self.nome},"
            f"cnpj={self.cnpj},"
            f"contato={self.contato})"
        )