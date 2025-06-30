from fastapi import FastAPI, HTTPException
from app.schemas import NotaRequest
from app.service import processar_emissao

app = FastAPI()

@app.post("/emitir_nota")
def emitir_nota(payload: NotaRequest):
    try:
        protocolo = processar_emissao(payload)
        return {"status": "sucesso", "protocolo": protocolo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
