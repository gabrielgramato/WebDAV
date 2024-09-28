import os

# Verifica se o arquivo 'users.json' existe
users_file = "users.json"
if not os.path.isfile(users_file):
    # Cria um arquivo 'users.json' vazio se não existir
    with open(users_file, 'w') as f:
        f.write('{}')  # Escreve um objeto JSON vazio

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
                "admin": {"password": "123"},  # Credenciais de acesso do admin
            },
        },
        "realm": "Link Informática",  # Definindo um realm
    },
    "verbose": 1,
}
