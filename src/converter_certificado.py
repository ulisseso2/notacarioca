from cryptography.hazmat.primitives.serialization import pkcs12, Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
import os

def converter_pfx_para_pem(pfx_path: str, senha: str) -> tuple[str, str]:
    with open(pfx_path, "rb") as f:
        pfx_data = f.read()

    private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
        pfx_data, senha.encode(), backend=default_backend()
    )

    cert_path = os.path.join("certs", "cert.pem")
    key_path = os.path.join("certs", "key.pem")
    os.makedirs("certs", exist_ok=True)

    with open(cert_path, "wb") as f:
        f.write(certificate.public_bytes(Encoding.PEM))

    with open(key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=NoEncryption()
        ))

    return cert_path, key_path
