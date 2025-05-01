---
title: Aprenda a implementar o conceito de Aliases no Docker Compose
description: Implemente o conceito de Aliases no Docker Compose
---

## Step-01: Introdução
- Implemente o [conceito de Aliases no Docker Compose](https://docs.docker.com/reference/compose-file/services/#aliases).

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
      frontend:
        aliases:
          - umsapp
          - dev-umsapp  
      backend: 
        aliases:
          - myspringapp
          - myapiservices
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]   # Supondo que /health seja o endpoint de verificação de integridade do app
      interval: 30s
      timeout: 10s
      retries: 3

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
cd aliases-demo

# Baixar imagens Docker e iniciar os containers
docker compose up -d 

# Listar containers Docker
docker compose ps
```

## Step-04: web-nginx: Verificar Conectividade com os Aliases de app-ums
```bash
# Conectar ao container web-nginx
docker exec -it ums-nginx /bin/bash

# Imagens baseadas em Debian/Ubuntu: Instalar iputils
apt-get update
apt-get install -y iputils-ping dnsutils

# Teste de Ping
ping app-ums (NOME DO SERVIÇO)
ping umsapp (ALIAS definido na REDE FRONTEND)
ping dev-umsapp (ALIAS definido na REDE FRONTEND)
Observação:
1. Todos os 3 devem resolver para o mesmo IP.

# Teste de nslookup
nslookup app-ums
nslookup umsapp
nslookup dev-umsapp
Observação:
1. Todos os 3 devem resolver para o mesmo IP.

# Teste de dig
dig app-ums
dig umsapp
dig dev-umsapp
Observação:
1. Todos os 3 devem resolver para o mesmo IP.

## TESTE NEGATIVO
ping myspringapp (ALIAS definido na REDE BACKEND)
Observação:
1. Deve falhar, pois o web-nginx não tem acesso à rede Backend.
```

## Step-05: db-mysql: Verificar Conectividade com os Aliases de app-ums
```bash
# Conectar ao container db-mysql
docker exec -it ums-mysqldb /bin/bash

# Imagens baseadas em Debian/Ubuntu: Instalar iputils
cat /etc/os-release
apt-get update
apt-get install -y iputils-ping dnsutils

# Imagens Oracle
cat /etc/os-release
microdnf install -y iputils bind-utils

# Teste de Ping
ping app-ums (NOME DO SERVIÇO)
ping myspringapp (ALIAS definido na REDE BACKEND)
ping myapiservices (ALIAS definido na REDE BACKEND)
Observação:
1. Todos os 3 devem resolver para o mesmo IP.

# Teste de nslookup
nslookup app-ums
nslookup myspringapp
nslookup myapiservices
Observação:
1. Todos os 3 devem resolver para o mesmo IP.

# Teste de dig
dig app-ums
dig myspringapp
dig myapiservices
Observação:
1. Todos os 3 devem resolver para o mesmo IP.

## TESTE NEGATIVO
ping umsapp (ALIAS definido na REDE FRONTEND)
Observação:
1. Deve falhar, pois o db-mysql não tem acesso à rede Frontend.
```

## Step-06: Limpeza
```bash
# Parar e remover containers
docker compose down -v

# Excluir imagens Docker
docker rmi $(docker images -q)
```