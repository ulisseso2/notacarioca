import requests
from app.config import CERT_PEM_PATH, KEY_PEM_PATH

def montar_envelope(xml: str) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <RecepcionarLoteRpsRequest xmlns="http://notacarioca.rio.gov.br/">
      <inputXML><![CDATA[{xml}]]></inputXML>
    </RecepcionarLoteRpsRequest>
  </soap:Body>
</soap:Envelope>"""

def enviar_para_prefeitura(xml_assinado: str):
    envelope = montar_envelope(xml_assinado)
    response = requests.post(
        url="https://notacarioca.rio.gov.br/WSNacional/nfse.asmx",
        data=envelope.encode("utf-8"),
        headers={
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": '"http://notacarioca.rio.gov.br/RecepcionarLoteRps"'
        },
        cert=(CERT_PEM_PATH, KEY_PEM_PATH),
        timeout=30
    )
    return response.text
