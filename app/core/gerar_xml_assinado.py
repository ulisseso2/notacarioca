from cryptography.hazmat.primitives.serialization import pkcs12
from signxml import XMLSigner, methods
from lxml import etree
from datetime import datetime

# Caminho do certificado .pfx e senha
pfx_path = "/home/ulisses/Área de trabalho/Folders/Certificados Digitais/1002153641DEGRAU.pfx"
pfx_password = b"123456"

# Carrega o arquivo PFX usando cryptography
with open(pfx_path, 'rb') as f:
    pfx_data = f.read()

private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
    data=pfx_data,
    password=pfx_password
)

# Serializa chave e cert para PEM (formato exigido pelo signxml)
from cryptography.hazmat.primitives import serialization

cert_pem = certificate.public_bytes(serialization.Encoding.PEM)
key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# XML base da NFSe (sem assinatura ainda)
data_emissao = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
xml = f'''<EnviarLoteRpsEnvio xmlns="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd">
  <LoteRps Id="Lote1">
    <NumeroLote>1</NumeroLote>
    <CpfCnpj>
      <Cnpj>28060747000154</Cnpj>
    </CpfCnpj>
    <InscricaoMunicipal>0639443</InscricaoMunicipal>
    <QuantidadeRps>1</QuantidadeRps>
    <ListaRps>
      <Rps>
        <InfRps Id="rps001">
          <IdentificacaoRps>
            <Numero>1</Numero>
            <Serie>RPS</Serie>
            <Tipo>1</Tipo>
          </IdentificacaoRps>
          <DataEmissao>{data_emissao}</DataEmissao>
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
            <ItemListaServico>08.02.03</ItemListaServico>
            <CodigoTributacaoMunicipio>08.02.03</CodigoTributacaoMunicipio>
            <Discriminacao>Aula de Apoio para Concurso</Discriminacao>
            <CodigoMunicipio>3304557</CodigoMunicipio>
          </Servico>
          <Prestador>
            <CpfCnpj>
              <Cnpj>28060747000154</Cnpj>
            </CpfCnpj>
            <InscricaoMunicipal>0639443</InscricaoMunicipal>
          </Prestador>
          <TomadorServico>
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
          </TomadorServico>
        </InfRps>
      </Rps>
    </ListaRps>
  </LoteRps>
</EnviarLoteRpsEnvio>'''

# Assina o XML
doc = etree.fromstring(xml.encode())
signer = XMLSigner(
    method=methods.enveloped,
    signature_algorithm="rsa-sha256",
    digest_algorithm="sha256"
)
signed = signer.sign(doc, key=key_pem, cert=cert_pem)

# Salva o arquivo assinado
with open("xml_assinado.xml", "wb") as f:
    f.write(etree.tostring(signed, pretty_print=True, xml_declaration=True, encoding='utf-8'))

print("✅ XML assinado salvo como xml_assinado.xml")
