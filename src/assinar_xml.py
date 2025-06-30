import os
from lxml import etree
from signxml import XMLSigner, methods
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend

# === CONFIGURAÇÕES ===
PFX_PATH = "certs/1002153641DEGRAU.pfx"
PFX_PASSWORD = "123456"
XML_ORIGINAL_PATH = "templates/rps_base.xml"
XML_ASSINADO_PATH = "signed/xml_assinado.xml"

def carregar_chaves(pfx_path: str, senha: str):
    with open(pfx_path, "rb") as f:
        pfx_data = f.read()

    private_key, certificate, _ = pkcs12.load_key_and_certificates(
        pfx_data, senha.encode(), backend=default_backend()
    )

    return private_key, certificate

def assinar_xml():
    print("🔐 Carregando chaves...")
    private_key, cert = carregar_chaves(PFX_PATH, PFX_PASSWORD)

    print("📄 Lendo XML base...")
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(XML_ORIGINAL_PATH, parser)
    root = tree.getroot()

    inf_rps = root.find(".//{http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd}InfRps")
    if inf_rps is None:
        raise Exception("❌ Tag <InfRps> não encontrada para assinatura.")

    print("✍️ Assinando XML...")
    signer = XMLSigner(
        method=methods.enveloped,
        signature_algorithm="rsa-sha256",
        digest_algorithm="sha256",
    )
    signed_info = signer.sign(
        inf_rps,
        key=private_key,
        cert=[cert],
        reference_uri=inf_rps.get("Id")
    )

    # Insere a assinatura após InfRps
    inf_rps.addnext(signed_info.find(".//{http://www.w3.org/2000/09/xmldsig#}Signature"))

    print("💾 Salvando XML assinado...")
    os.makedirs("signed", exist_ok=True)
    with open(XML_ASSINADO_PATH, "wb") as f:
        f.write(etree.tostring(root, pretty_print=True, encoding="utf-8", xml_declaration=True))

    print(f"✅ XML assinado salvo em: {XML_ASSINADO_PATH}")

if __name__ == "__main__":
    assinar_xml()
