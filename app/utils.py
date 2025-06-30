def montar_envelope(xml: str) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <RecepcionarLoteRpsRequest xmlns="http://notacarioca.rio.gov.br/">
      <inputXML><![CDATA[{xml}]]></inputXML>
    </RecepcionarLoteRpsRequest>
  </soap:Body>
</soap:Envelope>"""

def converter_pfx_para_pem(pfx_path, pfx_password):
    # converte para cert.pem e key.pem temporários
    return cert_path, key_path
