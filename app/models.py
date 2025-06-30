from pydantic import BaseModel

class NotaRequest(BaseModel):
    nome: str
    cpf: str
    endereco: str
    numero: str
    bairro: str
    cep: str
    municipio: str
    uf: str
    valor: float
    descricao: str
