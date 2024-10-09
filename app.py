import os
import sys

# Verifica se o arquivo 'config.py' existe antes de tentar importar
config_path = "config.py"
if not os.path.isfile(config_path):
    print(f"Arquivo '{config_path}' não encontrado. Executando hash.py para gerar uma nova chave e usuário.")
    os.system('python hash.py')  # Executa hash.py para gerar a chave e o usuário
    sys.exit(0)  # Sai do programa após executar o hash.py

# Tente importar a configuração
try:
    from config import config  # Importando a configuração do arquivo config.py
except Exception as e:
    print(f"Erro ao importar o arquivo 'config.py': {e}")
    sys.exit(1)

# Verifica se o arquivo 'secret.key' existe
secret_key_file = os.path.join("accounts", "secret.key")
if not os.path.isfile(secret_key_file):
    print("Arquivo 'secret.key' não encontrado. Executando hash.py para gerar uma nova chave e usuário.")
    os.system('python hash.py')  # Executa hash.py para gerar a chave e o usuário
    sys.exit(0)  # Sai do programa após executar o hash.py

# Continue com a inicialização do WsgiDAV
from wsgidav.wsgidav_app import WsgiDAVApp
from wsgiref.simple_server import make_server
from middleware import custom_middleware  # Importando o middleware

app = WsgiDAVApp(config)
app = custom_middleware(app)  # Integrando o middleware

if __name__ == "__main__":
    print(f"Servindo WebDAV em http://{config['host']}:{config['port']}")
    with make_server(config["host"], config["port"], app) as httpd:
        httpd.serve_forever()
