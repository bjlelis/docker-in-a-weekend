---
title: Aprenda sobre o conceito de Links no Docker Compose
description: Implemente o conceito de links no Docker Compose
---

## Step-01: Introdução
- Aprenda sobre [Links no Docker Compose](https://docs.docker.com/compose/how-tos/networking/#link-containers).

## Step-02: Revisar docker-compose.yaml
```yaml
name: ums-stack
services:
  web-nginx:
    image: nginx:latest 
    container_name: ums-nginx
    ports:
      - "8080:8080"  # O NGINX escuta na porta 8080 do host
    depends_on:
      app-ums:
        condition: service_healthy
        restart: true      
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf  # Configuração personalizada do NGINX
    networks:
      - frontend      
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/nginx-health"]  # Verifica se o NGINX está respondendo
      interval: 30s
      timeout: 10s
      retries: 3

  app-ums:
    image: ghcr.io/stacksimplify/usermgmt-webapp-v6:latest
    ports:
      - "8080"  # Apenas expõe a porta do container, permitindo que o Docker escolha a porta do host
    deploy:
      replicas: 1  # Escala o serviço para 1 instância       
    depends_on:
      db-mysql:
        condition: service_healthy
        restart: true
    environment:
      - DB_HOSTNAME=db-mysql
      - DB_PORT=3306
      - DB_NAME=webappdb
      - DB_USERNAME=root
      - DB_PASSWORD=dbpassword11
    networks:
      - frontend  
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]   # Supondo que /health seja o endpoint de verificação de integridade do app
      interval: 30s
      timeout: 10s
      retries: 3
    links:
      - db-mysql:myumsdb
      - db-mysql:mydevdb   

  db-mysql:
    container_name: ums-mysqldb
    image: mysql:8.0-bookworm
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: dbpassword11
      MYSQL_DATABASE: webappdb
    ports:
      - "3306:3306"
    volumes:
      - mydb:/var/lib/mysql
    networks:
      - backend        
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-pdbpassword11"]
      interval: 30s
      timeout: 10s
      retries: 3

  netshoot:
    image: nicolaka/netshoot
    container_name: ums-netshoot
    entrypoint: ["sleep", "infinity"]  # Mantém o container em execução para solução de problemas manual
    profiles: ["debug"]
    networks:
      - frontend
      - backend

volumes:
  mydb:

networks:
  frontend:
  backend:
```

## Step-03: Iniciar a Pilha
```bash
# Alterar para o diretório do projeto
cd links-demo

# Baixar imagens Docker e iniciar os containers
docker compose up -d 

# Listar containers Docker
docker compose ps
```

## Step-04: app-ums para db-mysql: Verificar Conectividade entre containers usando o conceito de LINKS
- Links permitem definir aliases extras pelos quais um serviço pode ser acessado a partir de outro serviço.
- Por padrão, qualquer serviço pode acessar outro serviço pelo nome do serviço (db-mysql, app-ums, web-nginx).
- No exemplo a seguir, db-mysql pode ser acessado a partir de app-ums pelos hostnames:
  - db-mysql (nome do serviço)
  - myumsdb (link criado em app-ums)
  - mydevdb (link criado em app-ums)
```bash
# Conectar ao container web-nginx
docker exec -it ums-stack-app-ums-1 /bin/bash

# Imagens baseadas em Debian/Ubuntu: Instalar iputils
apt-get update
apt-get install -y iputils-ping dnsutils

# Teste de nslookup
nslookup db-mysql
nslookup myumsdb
nslookup mydevdb
Observação:
1. db-mysql, myumsdb e mydevdb resolvem para o mesmo IP.

# Teste de dig
dig db-mysql
dig myumsdb
dig mydevdb
Observação:
1. db-mysql, myumsdb e mydevdb resolvem para o mesmo IP.

# Teste de ping
ping db-mysql
ping myumsdb
ping mydevdb

# Teste de telnet
telnet db-mysql 3306
telnet myumsdb 3306
telnet mydevdb 3306
```

## Step-05: Limpeza
```bash
# Parar e remover containers
docker compose down -v

# Excluir imagens Docker
docker rmi $(docker images -q)
```