from app.models import NotaRequest

def gerar_xml(dados: NotaRequest) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<EnviarLoteRpsEnvio xmlns="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd">
  <LoteRps Id="L1">
    <NumeroLote>...</NumeroLote>
    <Cnpj>28060747000154</Cnpj>
    <InscricaoMunicipal>0639443</InscricaoMunicipal>
    ...
    <Tomador>
      <IdentificacaoTomador>
        <CpfCnpj><Cpf>{dados.cpf}</CpfCnpj></CpfCnpj>
      </IdentificacaoTomador>
      <RazaoSocial>{dados.nome}</RazaoSocial>
      <Endereco>
        <Endereco>{dados.endereco}</Endereco>
        <Numero>{dados.numero}</Numero>
        <Bairro>{dados.bairro}</Bairro>
        <CodigoMunicipio>{dados.municipio}</CodigoMunicipio>
        <Uf>{dados.uf}</Uf>
        <Cep>{dados.cep}</Cep>
      </Endereco>
    </Tomador>
  </LoteRps>
</EnviarLoteRpsEnvio>
"""
