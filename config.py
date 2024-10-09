import os
import json  # Corrigindo o erro ao importar o módulo json

# Define o diretório para os arquivos de configuração
accounts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "accounts")

# Caminhos completos para os arquivos dentro da pasta 'accounts'
users_file = os.path.join(accounts_dir, "users.json")

# Carrega a configuração somente se o arquivo 'users.json' existir
if os.path.isfile(users_file):
    with open(users_file, 'r') as f:
        users = json.load(f)
else:
    print("Arquivo 'users.json' não encontrado. Execute o hash.py para criar um usuário.")
    users = {}  # Define um dicionário vazio caso o arquivo não exista

# Carrega a configuração do arquivo
config = {
    "host": "0.0.0.0",  # Servidor disponível em qualquer IP
    "port": 3222,  # Porta de acesso
    "provider_mapping": {
        "/": r"N:\\",  # Mapeia o caminho do sistema de arquivos
    },
    "simple_dc": {
        "user_mapping": {
            "/": {  # Mapeamento de usuários para o caminho "/"
                # Aqui podemos usar o conteúdo do 'users.json' quando ele existir
                "admin": users.get("admin", {"password": "mari.2401"}),  # Credenciais padrão caso não haja usuários
            },
        },
        "realm": "Link Informática",  # Definindo um realm
    },
    "verbose": 1,
}
