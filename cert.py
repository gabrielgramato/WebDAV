import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta, timezone

# Caminho da pasta para salvar os certificados
certs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certs")
cert_file = os.path.join(certs_dir, "cert.pem")
key_file = os.path.join(certs_dir, "key.pem")

def generate_ssl_cert():
    if not os.path.exists(certs_dir):
        os.makedirs(certs_dir)
        print(f"Pasta 'certs' criada em: {certs_dir}")

    # Gerando chave privada RSA
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Detalhes do certificado
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "SP"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Santa Isabel"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Link Informática LTDA"),
        x509.NameAttribute(NameOID.COMMON_NAME, "187.103.57.132"),  # IP do servidor
    ])

    # Gerando o certificado autoassinado
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc))  # Usando UTC
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=365))  # Certificado válido por 1 ano
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(key, hashes.SHA256(), default_backend())
    )

    # Salvando a chave privada
    with open(key_file, "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    # Salvando o certificado
    with open(cert_file, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print(f"Certificado SSL gerado com sucesso em {certs_dir}")

if __name__ == "__main__":
    generate_ssl_cert()
