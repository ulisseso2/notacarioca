# Arquivo: src/enviar_nfse.py
# Versão Final e Definitiva

import os
import requests
import html
from converter_certificado import converter_pfx_para_pem

# === CONFIGURAÇÕES ===
PFX_PATH = "certs/1002153641DEGRAU.pfx"
PFX_PASSWORD = "123456" # Lembre-se de usar a senha real do seu certificado
XML_ASSINADO_PATH = "signed/xml_assinado.xml"
URL = "https://notacarioca.rio.gov.br/WSNacional/nfse.asmx"


def montar_envelope(xml_interno: str) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    <RecepcionarLoteRpsRequest xmlns="http://notacarioca.rio.gov.br/">
      <inputXML><![CDATA[{xml_interno}]]></inputXML>
    </RecepcionarLoteRpsRequest>
  </soap:Body>
</soap:Envelope>"""


def enviar_com_requests(envelope: str, cert_path: str, key_path: str):
    """
    Envia a requisição SOAP com o SOAPAction correto para a Nota Carioca.
    """
    print("📡 Enviando requisição via requests...")

    cert = (cert_path, key_path)
    soap_action_com_aspas = '"http://notacarioca.rio.gov.br/RecepcionarLoteRps"'

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": soap_action_com_aspas
    }

    print("📤 Headers enviados:")
    for k, v in headers.items():
        print(f"{k}: {v}")

    try:
        response = requests.post(
            URL,
            data=envelope.encode("utf-8"),
            headers=headers,
            cert=cert,
            timeout=30
        )

        print(f"📬 Status da Resposta: {response.status_code}")
        print("📬 Resposta do Servidor (decodificada):")
        if response.text:
            print(response.text)
        else:
            print("[A resposta do servidor está vazia]")

    except requests.exceptions.SSLError as e:
        print("\n" + "="*50)
        print("❌ ERRO DE SSL/TLS ❌")
        print(f"Detalhes do erro: {e}")
        print("="*50 + "\n")
    except requests.exceptions.ConnectionError as e:
        print("\n" + "="*50)
        print("❌ ERRO DE CONEXÃO ❌")
        print(f"Detalhes do erro: {e}")
        print("="*50 + "\n")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado durante a requisição: {e}")


def enviar_nfse():
    """
    Função principal que orquestra todo o processo de envio.
    """
    print("🔐 Convertendo certificado PFX para PEM...")
    try:
        cert_path, key_path = converter_pfx_para_pem(PFX_PATH, PFX_PASSWORD)
    except Exception as e:
        print(f"Falha ao converter o certificado: {e}")
        return

    print("📄 Lendo e limpando o XML assinado...")
    try:
        xml_assinado = """<?xml version='1.0' encoding='utf-8'?>
<EnviarLoteRpsEnvio xmlns="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd">
  <LoteRps Id="Lote1">
    <NumeroLote>3</NumeroLote>
      <Cnpj>28060747000154</Cnpj>
    <InscricaoMunicipal>0639443</InscricaoMunicipal>
    <QuantidadeRps>1</QuantidadeRps>
    <ListaRps>
      <Rps>
        <InfRps Id="rps100000854">
          <IdentificacaoRps>
            <Numero>100000854</Numero>
            <Serie>RPS</Serie>
            <Tipo>1</Tipo>
          </IdentificacaoRps>
          <DataEmissao>2025-06-29T12:01:00</DataEmissao>
          <NaturezaOperacao>1</NaturezaOperacao>
          <OptanteSimplesNacional>2</OptanteSimplesNacional>
          <IncentivadorCultural>2</IncentivadorCultural>
          <Status>1</Status>
          <Servico>
            <Valores>
              <ValorServicos>100.00</ValorServicos>
              <IssRetido>2</IssRetido>
              <Aliquota>0.02</Aliquota>
            </Valores>
            <ItemListaServico>0802</ItemListaServico>
            <CodigoTributacaoMunicipio>041080203</CodigoTributacaoMunicipio>
            <Discriminacao>Serviços prestados: Aula de Apoio para Concurso</Discriminacao>
            <CodigoMunicipio>3304557</CodigoMunicipio>
          </Servico>
          <Prestador>
  
              <Cnpj>28060747000154</Cnpj>
     
            <InscricaoMunicipal>0639443</InscricaoMunicipal>
          </Prestador>
          <Tomador>
            <IdentificacaoTomador>
              <CpfCnpj>
                <Cpf>09063428723</Cpf>
              </CpfCnpj>
            </IdentificacaoTomador>
            <RazaoSocial>Ulisses Oliveira</RazaoSocial>
            <Endereco>
              <Endereco>Rua Exemplo</Endereco>
              <Numero>123</Numero>
              <Bairro>Centro</Bairro>
              <CodigoMunicipio>3304557</CodigoMunicipio>
              <Uf>RJ</Uf>
              <Cep>20000000</Cep>
            </Endereco>
          </Tomador>
        </InfRps>
        <ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
          <ds:SignedInfo>
            <ds:CanonicalizationMethod Algorithm="http://www.w3.org/2006/12/xml-c14n11"/>
            <ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/>
            <ds:Reference URI="#rps100000851">
              <ds:Transforms>
                <ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
                <ds:Transform Algorithm="http://www.w3.org/2006/12/xml-c14n11"/>
              </ds:Transforms>
              <ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
              <ds:DigestValue>UxuK8q8EWWB6C82/66yfXnoQauK1AqWC7xaVnuLfdCg=</ds:DigestValue>
            </ds:Reference>
          </ds:SignedInfo>
          <ds:SignatureValue>DhEbFViPa+ZAIn3OHpTuX0FM/H3swyXsJ0f1YLPc1hc2YPSMH+yWyZL4GEY9MLA7VQl6Y6IC0C+9giqvQiZ8fglrdiw8JPY9mJkwDLlVBUAW5qO5oVVATMW3wcyQgcqUXsl498IvWi84XffW9Jbzu4MZucmcPEmoYLckhfqcAZ/Cd99lrGs0MHIHUXt04wt4c3f+pdfQIkCjziH7AUZRfjrgCQpiW7ryKNMCZp0cQLmz7FXaEVePaqCH7bzmP2oLS+y5/Txp83VP/HHU436wH+SlVrfp4rx3DjB833uVbhdEhvgl07/vFzvjGPk+A1G9WIZ/LYlIZlvcExlP5UPRgg==</ds:SignatureValue>
          <ds:KeyInfo>
            <ds:X509Data>
              <ds:X509Certificate>MIIHjzCCBXegAwIBAgIIUPDvpjhtWBMwDQYJKoZIhvcNAQELBQAwczELMAkGA1UE
BhMCQlIxEzARBgNVBAoTCklDUC1CcmFzaWwxNjA0BgNVBAsTLVNlY3JldGFyaWEg
ZGEgUmVjZWl0YSBGZWRlcmFsIGRvIEJyYXNpbCAtIFJGQjEXMBUGA1UEAxMOQUMg
Q05ETCBSRkIgdjMwHhcNMjQxMTA1MDk0MDQ4WhcNMjUxMTA1MDk0MDQ4WjCCAQIx
CzAJBgNVBAYTAkJSMRMwEQYDVQQKEwpJQ1AtQnJhc2lsMQswCQYDVQQIEwJSSjEX
MBUGA1UEBxMOUklPIERFIEpBTkVJUk8xFzAVBgNVBAsTDjMwNTk4NDcyMDAwMTU5
MTYwNAYDVQQLEy1TZWNyZXRhcmlhIGRhIFJlY2VpdGEgRmVkZXJhbCBkbyBCcmFz
aWwgLSBSRkIxFjAUBgNVBAsTDVJGQiBlLUNOUEogQTExGTAXBgNVBAsTEHZpZGVv
Y29uZmVyZW5jaWExNDAyBgNVBAMTK0VESVRPUkEgREVHUkFVIENVTFRVUkFMIExU
REE6MjgwNjA3NDcwMDAxNTQwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIB
AQDuBND7TKWf+L8liZl35SMrOZ5AzzVbYtVYHGuyHWZf6djG7ITzFEvyoo9pX8sf
1mO/N6OMsOJg8BVJRMBwojIaE+VHO44PGuRdr5EEFglUezmBFY5Y5vPVGydZA5C2
gn5ruWR5VboKZfbY4eyEo1Wo2oSDpIK0vnYQP+r4RWvm5hl/8t500k8hwh9uzMSs
YSNJmhXA0B0iaqIz+rp/M1RlU1GaYBl92YHkljXqrXAyPddZ3TplSbZORyElhmEo
vmsGK5IEs8I5ECZ3JAtjvTP10t/MkfbaPZC/+ggxoH5IlJG5Y1ehufVvMQc5hYiB
5kp9ERSZZSDeApDXREu4wPQlAgMBAAGjggKUMIICkDAfBgNVHSMEGDAWgBRrHzQV
QRrqmx7KItLO3e+76TLKiTAOBgNVHQ8BAf8EBAMCBeAwZwYDVR0gBGAwXjBcBgZg
TAECATQwUjBQBggrBgEFBQcCARZEaHR0cDovL3JlcG9zaXRvcmlvLmFjc3BjYnJh
c2lsLm9yZy5ici9hYy1jbmRscmZiL2FjLWNuZGwtcmZiLWRwYy5wZGYwgaYGA1Ud
HwSBnjCBmzBLoEmgR4ZFaHR0cDovL3JlcG9zaXRvcmlvLmFjc3BjYnJhc2lsLm9y
Zy5ici9hYy1jbmRscmZiL2xjci1hYy1jbmRscmZidjUuY3JsMEygSqBIhkZodHRw
Oi8vcmVwb3NpdG9yaW8yLmFjc3BjYnJhc2lsLm9yZy5ici9hYy1jbmRscmZiL2xj
ci1hYy1jbmRscmZidjUuY3JsMF0GCCsGAQUFBwEBBFEwTzBNBggrBgEFBQcwAoZB
aHR0cDovL3JlcG9zaXRvcmlvLmFjc3BjYnJhc2lsLm9yZy5ici9hYy1jbmRscmZi
L2FjLWNuZGxyZmJ2NS5wN2IwgcEGA1UdEQSBuTCBtoEVQkVSRU1BUlRJTlNAR01B
SUwuQ09NoC8GBWBMAQMCoCYTJE1BUklaRVRFIFJJQkVJUk8gQ0FTVEFOSEVJUkEg
TUFSVElOU6AZBgVgTAEDA6AQEw4yODA2MDc0NzAwMDE1NKA4BgVgTAEDBKAvEy0y
NzEwMTk0NjgwMTQ2NTk3NzUzMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDCgFwYF
YEwBAwegDhMMMDAwMDAwMDAwMDAwMB0GA1UdJQQWMBQGCCsGAQUFBwMCBggrBgEF
BQcDBDAJBgNVHRMEAjAAMA0GCSqGSIb3DQEBCwUAA4ICAQBarBySCMkicA85pSPp
7IkRg15JA/L1cbTalCfMcVaClkKsqVhRqe3J1Ow2MaPNpiTOsY4oR6cKerVLTWvJ
X4gWF8qxiH6Ry9nqHrfMmPWgBvKiMkNqh/E1hnC9HClymJQebwPrO2zoV2FG/6VG
V18F1wBK5DR8IrvJXBEvoYWthQW+GXRf3unVl2imNrl1So93ucVFqb5JULslDaGb
IgCWhWpKzf4MG//b3akCfaIaTmUCdk7ZYhQJ99SGopNLiI5TDZdteadQp6LAT6qt
PDgQmAftQVQXtCL73BpFPszC4OWRAXYEdZx8+sTaE1xyb2ZzBRmKH0qARgH+hBAD
W438C7GUuRuPcCfc2SQZ+bANw9NjXXy1grLyV1iYgoYjsD0nFaqD8b1iKpQKYvu3
OLsi8MQSPNKCfLoJ5GWCGaZ3va8nr9YgkIm4/LGmtvaUyfIc/E87zufApLwon1Bs
e8rGa6c18XCUvTfuMuLqM8aZaAYsuiroRreaEp46nflutLXFQ+ks65oVt/lSWV93
/hy8mY5Y55J6+/s9A8o6G+d2Iw09FYS0zcj+JAmUpsN99bCEUBr6PvHd5HsGvz9v
wPlVhx4IAYJIHRHa8VASrzyc6vsi2JqO7TMqN3nsza0/zbMgRgpvALWRjjBm1KRy
+O2dVHxIEOypvTPdDMH6Yc29tA==
</ds:X509Certificate>
            </ds:X509Data>
          </ds:KeyInfo>
        </ds:Signature>
      </Rps>
    </ListaRps>
  </LoteRps>
</EnviarLoteRpsEnvio>
"""

        # --- LÓGICA DE LIMPEZA DO XML ---
        # 1. Remove o caractere BOM invisível, se ele existir no início do arquivo.
        if xml_assinado.startswith('\ufeff'):
            print("   -> ⚠️  Detectado e removido um BOM (Byte Order Mark) do XML.")
            xml_assinado = xml_assinado.lstrip('\ufeff')

        # 2. Remove espaços em branco ou linhas extras no início e no fim do conteúdo.
        xml_assinado = xml_assinado.strip()
        print("   -> ✅ XML lido e preparado para envio.")

    except FileNotFoundError:
        print(f"Erro: Arquivo XML não encontrado em '{XML_ASSINADO_PATH}'")
        os.remove(cert_path)
        os.remove(key_path)
        return

    print("📦 Montando envelope SOAP...")
    envelope = montar_envelope(xml_assinado)

    enviar_com_requests(envelope, cert_path, key_path)

    print("🗑️ Removendo arquivos de certificado temporários...")
    os.remove(cert_path)
    os.remove(key_path)
    print("✅ Processo finalizado.")


if __name__ == "__main__":
    enviar_nfse()