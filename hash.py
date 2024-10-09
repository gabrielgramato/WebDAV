import bcrypt
import getpass
import json
import os
import sys
from cryptography.fernet import Fernet

# Define o diretório onde os arquivos serão armazenados
accounts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "accounts")

# Verifica se o diretório 'accounts' existe, caso contrário, cria o diretório
if not os.path.exists(accounts_dir):
    os.makedirs(accounts_dir)
    print(f"Pasta 'accounts' criada em: {accounts_dir}")

# Caminhos completos para os arquivos dentro da pasta 'accounts'
users_file = os.path.join(accounts_dir, "users.json")
secret_key_file = os.path.join(accounts_dir, "secret.key")

def generate_secret_key():
    """Gera uma nova chave secreta e a salva em 'secret.key'."""
    key = Fernet.generate_key()
    with open(secret_key_file, "wb") as key_file:
        key_file.write(key)
    print("Chave gerada e salva como 'secret.key'.")

def generate_password_hash(username):
    """Gera um hash da senha fornecida e salva o usuário no arquivo 'users.json'."""
    # Lê a senha do usuário sem exibir
    password = getpass.getpass(f"Digite a nova senha para '{username}': ")
    
    # Gera o hash da senha
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Carrega ou cria o arquivo 'users.json' somente quando um usuário for criado
    try:
        if os.path.exists(users_file):
            with open(users_file, "r") as f:
                users = json.load(f)
        else:
            users = {}  # Se o arquivo não existe, cria um dicionário vazio

        # Adiciona ou atualiza o usuário no dicionário
        users[username] = {"password": hashed_password.decode('utf-8')}

        # Salva os dados atualizados de volta no arquivo, formatando o JSON com indentação
        with open(users_file, "w") as f:
            json.dump(users, f, indent=4)

        print(f"Usuário '{username}' criado e salvo em 'users.json'.")
    
    except Exception as e:
        print(f"Erro ao salvar o usuário: {e}")

if __name__ == "__main__":
    created_first_user = False  # Flag para verificar se o primeiro usuário foi criado

    while True:
        username = input("Digite o nome de usuário: ")
        generate_password_hash(username)

        # Se o primeiro usuário foi criado, gera a chave secreta
        if not created_first_user:
            if not os.path.exists(secret_key_file):
                generate_secret_key()
            created_first_user = True  # Marca que o primeiro usuário foi criado

        # Pergunta ao usuário se deseja criar outro
        another = input("Deseja criar outro usuário? (s/n): ").strip().lower()
        if another != 's':
            break

    # Se o usuário não quiser criar mais, chama o app.py
    print("Iniciando o app.py...")
    os.system("python app.py")
