from pydantic import BaseModel

class Endereco(BaseModel):
    logradouro: str
    numero: str
    bairro: str
    codigo_municipio: str
    uf: str
    cep: str

class Tomador(BaseModel):
    nome: str
    cpf: str
    endereco: Endereco

class NotaRequest(BaseModel):
    tomador: Tomador
    valor: float
    descricao: str
