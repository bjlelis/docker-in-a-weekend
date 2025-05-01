---
title: Aprenda a usar a flag "--build" no Docker Compose
description: Aprenda a usar a flag "--build" no Docker Compose
---

## Step-01: Introdução
- Aprenda a usar o comando `docker compose up --build`.

## Entendendo a flag --build
```bash
# Docker Compose com a flag --build
docker compose up --build -d
```

### Flag `--build` no comando `docker compose up`

- **Constrói Imagens Antes de Iniciar os Containers**: A flag `--build` força o Docker Compose a construir ou reconstruir as imagens definidas no arquivo `docker-compose.yml` antes de iniciar os containers. Isso é particularmente útil se você fez alterações no Dockerfile ou em outros componentes que afetam a imagem, como atualizações de código ou mudanças em variáveis de ambiente.

- **Não é Necessário Executar Manualmente `docker compose build`**: Normalmente, se você modificar seu Dockerfile ou código da aplicação, precisaria primeiro executar `docker compose build` para reconstruir as imagens e, em seguida, usar `docker compose up` para iniciar os containers. Usar `--build` combina esses passos em um único comando, tornando conveniente construir e iniciar os containers automaticamente.

- **Casos de Uso**:
  - **Alterações no Código**: Se você atualizou o código da aplicação ou modificou arquivos copiados para a imagem.
  - **Alterações no Dockerfile**: Se você alterou instruções no Dockerfile, como adicionar uma nova dependência ou atualizar a imagem base.
  - **Atualizações de Ambiente**: Se você modificou argumentos de build (`ARG`) ou variáveis de ambiente que afetam a imagem durante o processo de build.

- **Construção Automática vs. Manual**: Sem a flag `--build`, o comando `docker compose up` usará a imagem existente, se já tiver sido construída. Ele não verificará alterações no Dockerfile ou outras dependências que fazem parte da imagem. A flag `--build` garante que a imagem seja reconstruída, independentemente de já ter sido construída anteriormente.

---

## Step-02: Revisar Aplicação de Exemplo
- Pasta: python-app
- **Arquivo: app.py**
```py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "V1: Hello, Docker Compose Build Demo"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

- **Arquivo: requirements.txt**
```txt
flask
```

- **Arquivo: Dockerfile**
```Dockerfile
# Usar a imagem oficial do Python do Docker Hub
FROM python:slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo de requisitos e instalar as dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar o conteúdo do diretório atual para o container em /app
COPY . .

# Expor a aplicação na porta 5000
EXPOSE 5000

# Executar a aplicação
CMD ["python", "app.py"]
```

---

## Step-03: Revisar docker-compose.yaml
```yaml
services:
  web:
    image: my-python-app:latest  # Nome da imagem Docker
    container_name: my-python-container  # Nome do container
    build: 
      context: ./python-app  
      dockerfile: Dockerfile  # Dockerfile a ser usado para construir a imagem
    ports:
      - "5000:5000"
```

---

## Step-04: Iniciar a Pilha e Verificar
```bash
# Alterar para o diretório do projeto
cd build-demo

# Baixar imagens Docker e iniciar os containers
docker compose up --build -d 

# Listar containers Docker
docker compose ps

# Listar imagens Docker
docker images
Observação:
1. Verifique a seção "CREATED" da imagem Docker.

# Acessar a aplicação
http://localhost:5000
Observação:
1. A versão V1 da aplicação será exibida.
```

---

## Step-05: Alterar o Código para a Versão V2
```py
# Atualizar app.py
return "V2: Hello, Docker Compose Build Demo"
```

---

## Step-06: Implantar a Versão V2 da Aplicação
```bash
# Alterar para o diretório do projeto
cd build-demo

# Reconstruir imagens Docker e iniciar os containers
docker compose up --build -d 

# Listar imagens Docker
docker images
Observação:
1. Verifique a seção "CREATED" da imagem Docker.
2. Uma nova imagem Docker será criada.

# Listar containers Docker
docker compose ps
Observação:
1. O container será recriado com a nova imagem Docker.

# Acessar a aplicação
http://localhost:5000
Observação:
1. A versão V2 da aplicação será exibida.
```

---

## Step-07: Limpeza
```bash
# Parar e remover containers
docker compose down

# Excluir imagens Docker
docker rmi $(docker images -q)
```