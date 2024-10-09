import os
import ssl
import subprocess
from wsgiref.simple_server import make_server

# Verifica se o certificado SSL existe
certs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certs")
cert_file = os.path.join(certs_dir, "cert.pem")
key_file = os.path.join(certs_dir, "key.pem")

if not os.path.exists(cert_file) or not os.path.exists(key_file):
    print("Certificado SSL não encontrado. Gerando certificado SSL...")
    subprocess.run(['python', 'cert.py'], check=True)

# Configuração SSL usando SSLContext
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=cert_file, keyfile=key_file)

# Caminho do arquivo index.html
html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

# Função WSGI para servir o arquivo index.html
def simple_app(environ, start_response):
    path = environ.get('PATH_INFO', '')
    
    # Serve o arquivo index.html apenas na raiz
    if path == '/' or path == '/index.html':
        try:
            with open(html_file, "rb") as f:
                content = f.read()
            status = '200 OK'
            headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content)))]
            start_response(status, headers)
            return [content]
        except FileNotFoundError:
            status = '404 Not Found'
            start_response(status, [('Content-Type', 'text/plain')])
            return [b'File not found']
    else:
        # Responde com 404 para qualquer outro caminho
        status = '404 Not Found'
        start_response(status, [('Content-Type', 'text/plain')])
        return [b'Page not found']

# Configurando o servidor com HTTPS
with make_server('', 3222, simple_app) as httpd:
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print("Servindo WebDAV em https://0.0.0.0:3222")
    httpd.serve_forever()
