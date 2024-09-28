import bcrypt
import getpass
import json
import os
import sys
from cryptography.fernet import Fernet

def generate_secret_key():
    """Gera uma nova chave secreta e a salva em 'secret.key'."""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Chave gerada e salva como 'secret.key'.")

def generate_password_hash(username):
    """Gera um hash da senha fornecida e salva o usuário no arquivo 'users.json'."""
    # Lê a senha do usuário sem exibir
    password = getpass.getpass(f"Digite a nova senha para '{username}': ")
    
    # Gera o hash da senha
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Salva o usuário e hash no arquivo 'users.json'
    users_file = "users.json"
    try:
        # Lê os dados existentes do arquivo
        if os.path.exists(users_file):
            with open(users_file, "r") as f:
                users = json.load(f)
        else:
            users = {}

        # Adiciona ou atualiza o usuário no dicionário
        users[username] = {"password": hashed_password.decode('utf-8')}

        # Salva os dados atualizados de volta no arquivo, formatando o JSON com indentação
        with open(users_file, "w") as f:
            json.dump(users, f, indent=4)  # Adicionando indentação para melhor legibilidade

        print("Hash gerado e salvo em 'users.json'.")
    
    except Exception as e:
        print(f"Erro ao salvar o hash: {e}")

if __name__ == "__main__":
    # Pergunta se deve criar um usuário antes de gerar a chave
    while True:
        username = input("Digite o nome de usuário: ")
        generate_password_hash(username)

        # Gera a chave secreta após a criação do primeiro usuário
        if not os.path.exists("secret.key"):
            generate_secret_key()

        # Pergunta ao usuário se deseja criar outro
        another = input("Deseja criar outro usuário? (s/n): ").strip().lower()
        if another != 's':
            break

    # Se o usuário não quiser criar mais, chama o app.py
    print("Iniciando o app.py...")
    os.system("python app.py")
