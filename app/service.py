from app.xml_builder import gerar_xml
from app.signer import assinar_xml
from app.sender import enviar_para_prefeitura
from app.settings import get_certificados

def processar_emissao(payload):
    certificados = get_certificados()

    xml = gerar_xml(payload)
    xml_assinado = assinar_xml(xml, certificados)
    protocolo = enviar_para_prefeitura(xml_assinado, certificados)

    return protocolo
