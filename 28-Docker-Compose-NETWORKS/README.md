---
title: "Domine Redes Docker Usando Docker Compose para Implantação Segura de Aplicações Multi-Camadas"
description: "Aprenda a implantar e gerenciar uma aplicação multi-camadas de forma segura usando Docker Compose com redes separadas para frontend e backend, garantindo isolamento, descoberta de serviços e balanceamento de carga."
---

# Domine Redes Docker Usando Docker Compose para Implantação Segura de Aplicações Multi-Camadas

---

## Step-01: Introdução

Esta configuração demonstra um típico setup de aplicação multi-camadas:
- `web-nginx` (frontend) se comunica com `app-ums` pela rede `frontend`, atuando como um proxy reverso.
- `app-ums` se comunica com `db-mysql` pela rede `backend`, garantindo que o banco de dados esteja isolado do ambiente externo.
- A separação das redes (`frontend` e `backend`) assegura que os serviços interajam apenas com aqueles necessários, proporcionando isolamento e segurança.

- **frontend**: Os serviços `web-nginx` e `app-ums` estão conectados a esta rede, permitindo que se comuniquem diretamente. Esta rede é usada para a comunicação entre o proxy reverso (`web-nginx`) e o aplicativo web (`app-ums`).
  
- **backend**: Os serviços `app-ums` e `db-mysql` estão conectados a esta rede. A rede backend facilita a comunicação entre o aplicativo (`app-ums`) e o banco de dados (`db-mysql`). O serviço `db-mysql` não é acessível pelo `web-nginx`, pois está conectado apenas à rede `backend`, garantindo um nível de segurança ao isolar o banco de dados dos serviços voltados para o exterior.

As redes fornecem um mecanismo interno de descoberta de serviços baseado em DNS, permitindo que os serviços se comuniquem usando nomes de serviço em vez de endereços IP. Por exemplo, `app-ums` pode acessar o container `db-mysql` referindo-se a ele como `db-mysql` (via a variável de ambiente `DB_HOSTNAME`).

---

## Step-02: Revisar docker-compose.yaml

```yaml
name: ums-stack
services:
  web-nginx:
    image: nginx:latest 
    container_name: ums-nginx
    ports:
      - "8080:8080"
    depends_on:
      - app-ums
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    networks:
      - frontend      

  app-ums:
    image: ghcr.io/stacksimplify/usermgmt-webapp-v6:latest
    ports:
      - "8080"
    deploy:
      replicas: 2
    depends_on:
      - db-mysql
    environment:
      - DB_HOSTNAME=db-mysql
      - DB_PORT=3306
      - DB_NAME=webappdb
      - DB_USERNAME=root
      - DB_PASSWORD=dbpassword11
    networks:
      - frontend  
      - backend

  db-mysql:
    container_name: ums-mysqldb
    image: mysql:8.0-bookworm
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: dbpassword11
      MYSQL_DATABASE=webappdb
    ports:
      - "3306:3306"
    volumes:
      - mydb:/var/lib/mysql
    networks:
      - backend        

volumes:
  mydb:

networks:
  frontend:
  backend:
```

---

## Step-03: Iniciar a Pilha

```bash
# Baixar imagens Docker e iniciar os containers
docker compose up -d 

# Listar containers Docker
docker compose ps
```

---

## Step-04: Verificar e Inspecionar Redes Docker

```bash
# Listar redes Docker
docker network ls

# Inspecionar rede Docker específica - FRONTEND
docker network inspect ums-stack_frontend

# Inspecionar rede Docker específica - BACKEND
docker network inspect ums-stack_backend
```

---

## Step-05: web-nginx: Verificar Conectividade Entre Containers a partir do web-nginx

### 1. **Comunicação Entre Serviços: `web-nginx` e `app-ums`**:
- `web-nginx` atua como um proxy reverso, encaminhando requisições recebidas na porta 8080 do host para `app-ums`. Como ambos os serviços compartilham a rede `frontend`, `web-nginx` pode resolver e acessar `app-ums` pelo nome do container (`app-ums`).

### 2. **Uso da Rede pelo `web-nginx` (Proxy Reverso Nginx)**:
- Conectado à rede `frontend`.
- Encaminha o tráfego recebido da porta 8080 do host para o serviço `app-ums`. Como ambos estão na mesma rede `frontend`, `web-nginx` pode acessar `app-ums` pelo nome do container.
- **Sem acesso ao `db-mysql`**: Como `web-nginx` não está conectado à rede `backend`, ele não pode se comunicar diretamente com o serviço de banco de dados, garantindo que o banco permaneça isolado.

```bash
# Conectar ao container web-nginx
docker exec -it ums-nginx /bin/sh

# Imagens baseadas em Alpine: Instalar iputils
apk update
apk add iputils bind-tools

# Imagens baseadas em Debian/Ubuntu: Instalar iputils
apt-get update
apt-get install -y iputils-ping dnsutils

# Testar conectividade com serviços
ping web-nginx
ping app-ums
ping db-mysql

# Observação:
# 1. web-nginx e app-ums funcionarão.
# 2. db-mysql falhará, pois NÃO HÁ ACESSO à rede backend.

# Consultar serviços com nslookup
nslookup web-nginx
nslookup app-ums
nslookup db-mysql

# Consultar serviços com dig
dig web-nginx
dig app-ums
dig db-mysql
```

---

## Step-06: app-ums: Verificar Conectividade Entre Containers a partir do app-ums

### 1. **Comunicação Entre Serviços: `app-ums` e `db-mysql`**:
- `app-ums` se comunica com `db-mysql` usando o hostname `db-mysql` e a porta `3306`. Ambos os serviços estão conectados à rede `backend`, permitindo que `app-ums` resolva `db-mysql` via DNS sem expor o banco de dados à rede externa.

### 2. **Uso da Rede pelo `app-ums` (Aplicativo Web de Gerenciamento de Usuários)**:
- Conectado às redes `frontend` e `backend`.
- Este serviço pode se comunicar com:
  - **`web-nginx`** pela rede `frontend`.
  - **`db-mysql`** pela rede `backend` usando a variável de ambiente `DB_HOSTNAME=db-mysql`.
- `app-ums` escala para duas réplicas, criando duas instâncias do aplicativo. Todas as réplicas compartilham as mesmas redes e podem acessar `db-mysql` pela rede backend.

```bash
# Conectar ao container app-ums (uma das réplicas)
docker exec -it --user root ums-stack-app-ums-1 /bin/bash

# Instalar iputils em imagens baseadas em Debian/Ubuntu
apt-get update
apt-get install -y iputils-ping dnsutils

# Testar conectividade com serviços
ping web-nginx
ping app-ums
ping db-mysql

# Consultar serviços com nslookup
nslookup web-nginx
nslookup app-ums
nslookup db-mysql

# Consultar serviços com dig
dig web-nginx
dig app-ums
dig db-mysql
```

---

## Step-07: db-mysql: Verificar Conectividade Entre Containers a partir do db-mysql

### 1. **Uso da Rede pelo `db-mysql` (Banco de Dados MySQL)**:
- Conectado apenas à rede `backend`.
- Isolado de serviços externos como `web-nginx`, aumentando a segurança ao limitar o acesso apenas ao `app-ums`, que também está na rede `backend`.
- O banco de dados escuta na porta 3306, mas apenas o serviço `app-ums` pode acessá-lo internamente pela rede `backend`.

```bash
# Conectar ao container db-mysql
docker exec -it ums-mysqldb /bin/bash

# Instalar iputils em imagens baseadas em Debian/Ubuntu
cat /etc/os-release
apt-get update
apt-get install -y iputils-ping dnsutils

# Testar conectividade com serviços
ping web-nginx
ping app-ums
ping db-mysql

# Consultar serviços com nslookup
nslookup web-nginx
nslookup app-ums
nslookup db-mysql

# Consultar serviços com dig
dig web-nginx
dig app-ums
dig db-mysql
```

---

## Step-08: Limpeza

```bash
# Parar e remover containers
docker compose down -v

# Excluir imagens Docker
docker rmi $(docker images -q)
```

---

## Conclusão

### 1. **Redes Isoladas e Seguras**
- **Isolamento do Banco de Dados**: `db-mysql` está conectado apenas à rede `backend`, isolando-o do serviço `web-nginx` para maior segurança.
- **Sem Rede do Host**: Os serviços se comunicam internamente via redes Docker, reduzindo a exposição dos serviços ao mundo externo.

### 2. **Descoberta de Serviços Usando DNS**
- Cada serviço em uma rede Docker pode ser acessado pelo nome do serviço. As redes Docker fornecem um serviço DNS embutido, facilitando o gerenciamento e a escalabilidade de aplicações multi-container.

---

**Feliz Dockerização!**