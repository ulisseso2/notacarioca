import os
from app.utils import converter_pfx_para_pem

def get_certificados():
    cert_path, key_path = converter_pfx_para_pem(
        pfx_path="certs/seu_certificado.pfx",
        pfx_password=os.getenv("PFX_PASSWORD")
    )
    return {"cert_path": cert_path, "key_path": key_path}
