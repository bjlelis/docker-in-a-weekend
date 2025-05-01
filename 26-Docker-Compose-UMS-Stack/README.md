---
title: "Implantar WebApp de Gerenciamento de Usuários e Banco de Dados MySQL Usando Docker Compose"
description: "Guia passo a passo para implantar uma pilha UMS com MySQL usando Docker Compose para armazenamento persistente de dados e gerenciamento de containers."
---

# Implantar Pilha UMS (Aplicativo Web de Gerenciamento de Usuários com Banco de Dados MySQL) Usando Docker Compose

---

## Step-01: Introdução

Neste tutorial, mostraremos como implantar um **Aplicativo Web de Gerenciamento de Usuários (UMS)** junto com um **banco de dados MySQL** usando **Docker Compose**. A pilha UMS é composta por:

1. **Banco de Dados MySQL**: Backend para armazenar dados de usuários.
2. **WebApp UMS**: Um aplicativo web que se conecta ao banco de dados MySQL para gerenciar usuários, incluindo operações de login, criação e listagem.

---

## Step-02: Pré-requisitos

Certifique-se de que você tenha as seguintes ferramentas instaladas no seu sistema:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Step-03: Estrutura do Projeto

```bash
ums-stack/
├── docker-compose.yaml   # Arquivo de configuração do Docker Compose
```

---

## Step-04: Serviços

### Serviço MySQL:

- Usa a imagem oficial `mysql:8.0` do Docker Hub.
- Configura o banco de dados com variáveis de ambiente.
- Expõe o serviço MySQL na porta `3306`.
- Armazena os dados do MySQL em um volume nomeado do Docker (`mydb`) para garantir a persistência dos dados.

### Serviço WebApp UMS:

- Usa a imagem `ghcr.io/stacksimplify/usermgmt-webapp-v6:latest` para o Aplicativo Web de Gerenciamento de Usuários.
- Conecta-se ao serviço de banco de dados MySQL para operações de backend.
- Expõe o WebApp UMS na porta `8080` da máquina host.

### docker-compose.yaml

```yaml
name: ums-stack
services:
  myumsapp:
    container_name: ums-app
    image: ghcr.io/stacksimplify/usermgmt-webapp-v6:latest
    ports:
      - "8080:8080"        
    depends_on:
      - mysql
    environment:
      - DB_HOSTNAME=mysql
      - DB_PORT=3306
      - DB_NAME=webappdb
      - DB_USERNAME=root
      - DB_PASSWORD=dbpassword11
  mysql:
    container_name: ums-mysqldb
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: dbpassword11
      MYSQL_DATABASE=webappdb
    ports:
      - "3306:3306"
    volumes:
      - mydb:/var/lib/mysql
volumes:
  mydb:
```

### Configuração Principal

#### Serviço WebApp UMS: `myumsapp`

- **`DB_HOSTNAME`**: O hostname do container MySQL, definido como `mysql`.
- **`DB_PORT`**: Porta do MySQL, definida como `3306`.
- **`DB_NAME`, `DB_USERNAME`, `DB_PASSWORD`**: Detalhes de conexão com o banco de dados para o WebApp UMS.

#### Serviço MySQL: `mysql`

- **`MYSQL_ROOT_PASSWORD`**: Senha root para o MySQL.
- **`MYSQL_DATABASE`**: Pré-configura o banco de dados `webappdb` para o WebApp UMS.

### Explicação dos Volumes

- **`mydb`**: Um volume nomeado do Docker para armazenamento persistente, garantindo que os dados do banco de dados MySQL persistam mesmo após reinicializações ou remoções de containers.

---

## Step-05: Como Iniciar a Pilha UMS

Siga os passos abaixo para iniciar a pilha UMS:

```bash
# Alterar para o diretório do projeto
cd ums-stack

# Iniciar a pilha UMS em modo detached
docker compose up -d
```

- A flag `-d` executa os serviços em modo detached, permitindo que eles rodem em segundo plano.

---

## Step-06: Verificar os Serviços

Para garantir que os serviços MySQL e WebApp UMS estão em execução:

```bash
# Listar containers Docker em execução
docker compose ps
```

Para visualizar os logs de ambos os serviços:

```bash
# Ver logs com docker compose
docker compose logs -f <NOME-DO-SERVIÇO>
docker compose logs -f mysql
docker compose logs -f myumsapp

# Ver logs usando nomes dos containers
docker logs -f <NOME-DO-CONTAINER-OU-ID>
docker logs -f ums-mysqldb
docker logs -f ums-app
```

---

## Step-07: Acessando o WebApp UMS

1. Abra seu navegador e navegue até `http://localhost:8080`.
2. Use as credenciais padrão para fazer login:
   - **Usuário**: `admin101`
   - **Senha**: `password101`
3. Após o login, você pode:
   - Visualizar uma lista de usuários.
   - Criar novos usuários.
   - Testar a funcionalidade de login com os novos usuários criados.

---

## Step-08: Conectar ao Container MySQL

Para inspecionar ou interagir com o banco de dados MySQL, conecte-se ao container MySQL:

```bash
# Conectar ao container MySQL
docker exec -it ums-mysqldb mysql -u root -pdbpassword11
```

Uma vez no shell do MySQL, você pode executar consultas SQL para visualizar o banco de dados `webappdb`:

```bash
mysql> show schemas;
mysql> use webappdb;
mysql> show tables;
mysql> select * from user;
```

---

## Step-09: Verificar Comunicação entre Containers Usando Nomes de Serviço e DNS

```bash
# Listar containers Docker em execução
docker compose ps

# Conectar ao container ums-app
docker exec -it ums-app /bin/bash

# Testar DNS - myumsapp
nslookup <NOME-DO-SERVIÇO>
nslookup myumsapp
dig myumsapp

# Testar DNS - mysql
nslookup <NOME-DO-SERVIÇO>
nslookup mysql
dig mysql
```

---

## Step-10: Parar e Limpar

Quando terminar, pare e remova os containers em execução:

```bash
# Parar e remover os containers
docker compose down
```

Para remover o volume MySQL também (opcional):

```bash
# Parar containers e remover volumes
docker compose down -v

# Listar volumes Docker para confirmar a remoção
docker volume ls
```

**Observação**: O comando `docker compose down -v` remove tanto os containers quanto o volume nomeado `mydb`, excluindo os dados persistentes.

---

## Conclusão

Neste tutorial, implantamos com sucesso um **banco de dados MySQL** e um **WebApp de Gerenciamento de Usuários** usando Docker Compose. Configuramos o banco de dados MySQL para armazenamento persistente e conectamos o WebApp para interagir com ele. Esta configuração pode ser escalada ou estendida com serviços adicionais.

---

## Recursos Adicionais

- [Documentação do Docker Compose](https://docs.docker.com/compose/)
- [Imagem MySQL no Docker Hub](https://hub.docker.com/_/mysql)
- [Imagem Docker do WebApp de Gerenciamento de Usuários](https://github.com/users/stacksimplify/packages/container/package/usermgmt-webapp-v6)
- [Gerenciamento de Volumes Docker](https://docs.docker.com/storage/volumes/)
- [Rede Docker](https://docs.docker.com/network/)

---

**Feliz Dockerização!**