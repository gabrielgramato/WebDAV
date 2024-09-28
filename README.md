# WebDAV
 Este projeto configura um servidor WebDAV para facilitar o compartilhamento de arquivos pela web, proporcionando um ambiente seguro e confiável para armazenar e acessar dados remotamente. Antes de iniciar, ele verifica a existência dos arquivos de configuração essenciais (config.py e secret.key). Se esses arquivos não existirem, o sistema executa o script hash.py para criar uma nova chave secreta e permitir a criação de usuários, garantindo que o servidor esteja sempre preparado para operações seguras.

## Preparando Ambiente Windows:

```
⚠️ Esta instalação foi focada para Windows Server 2019 Standard
```

```
# Instale do Java:
https://www.java.com/pt-BR/download/ie_manual.jsp

# Instale o do GIT:
https://git-scm.com/downloads/win

# Instale do Node:
https://nodejs.org/en/download/prebuilt-installer
```

## Instalação do WebDAV:

```
⚠️ Execute linha por linha!

# Download WebDAV:
cd C:\
git clone https://github.com/gabrielgramato/WebDAV.git
cd WebDAV\
pip install bcrypt cryptography wsgidav
python app.py

# Quando Reiniciar o Servidor:
cd C:\WebDAV\
python app.py
```
