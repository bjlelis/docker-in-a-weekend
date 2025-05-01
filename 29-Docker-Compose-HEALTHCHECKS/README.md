---
title: Aprenda Docker Compose Healthchecks
description: Implemente Healthchecks no Docker Compose
---

## Step-01: Introdução
- Implemente verificações de integridade (Healthchecks) para os 3 serviços no arquivo Docker Compose.

## Step-02: Revisar nginx.conf
```conf
events { }

http {
  # Resolvedor DNS interno do Docker, configura o bloco upstream para resolver o nome do serviço para múltiplos IPs
  resolver 127.0.0.11 ipv6=off;  
  
  upstream app-ums {
    # O Docker resolverá automaticamente 'app-ums' para os containers
    server app-ums:8080;  

    # Use o endereço IP do cliente para persistência de sessão (NECESSÁRIO PARA O UMS WEBAPP)
    ip_hash;  # Desative para ver como o balanceamento de carga funciona acessando a API http://localhost:8080/hello1
  }

  server {
    listen 8080;

    # Verificação de integridade para o NGINX (página estática ou resposta simples)
    location /nginx-health {
        return 200 "NGINX is healthy!";
        add_header Content-Type text/plain;
    } 

    # Status do NGINX
    location /nginx_status {
        stub_status on;              # Habilitar o módulo stub_status
        #allow 127.0.0.1;             # Permitir requisições do localhost
        #deny all;                    # Negar todas as outras IPs
    }

    # Proxypass para nosso Aplicativo Web de Gerenciamento de Usuários (UMS App)
    location / {
      proxy_pass http://app-ums;
    }
  }
}
```

## Step-03: Revisar docker-compose.yaml
```yaml
name: ums-stack
services:
  web-nginx:
    image: nginx:latest 
    container_name: ums-nginx
    ports:
      - "8080:8080"  # O NGINX escuta na porta 8080 do host
    depends_on:
      - app-ums
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
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]   # Supondo que /health seja o endpoint de verificação de integridade do app
      interval: 30s
      timeout: 10s
      retries: 3

  db-mysql:
    container_name: ums-mysqldb
    image: mysql:8.0
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

volumes:
  mydb:

networks:
  frontend:
  backend:
```

## Step-04: Iniciar a Pilha
```bash
# Alterar para o diretório do projeto
cd healthcheck-demo

# Baixar imagens Docker e iniciar os containers
docker compose up -d 

# Listar containers Docker
docker compose ps
Observação:
1. Você deve ver todos os containers mostrando o status "healthy".

# Exemplo de saída
kalyan-mini2:healthchecks-demo kalyan$ docker compose ps
NAME                  IMAGE                                             COMMAND                  SERVICE     CREATED          STATUS                    PORTS
ums-mysqldb           mysql:8.0                                         "docker-entrypoint.s…"   db-mysql    39 seconds ago   Up 38 seconds (healthy)   0.0.0.0:3306->3306/tcp, 33060/tcp
ums-nginx             nginx:latest                                      "/docker-entrypoint.…"   web-nginx   39 seconds ago   Up 38 seconds (healthy)   80/tcp, 0.0.0.0:8080->8080/tcp
ums-stack-app-ums-1   ghcr.io/stacksimplify/usermgmt-webapp-v6:latest   "catalina.sh run"        app-ums     39 seconds ago   Up 38 seconds (healthy)   0.0.0.0:63848->8080/tcp
kalyan-mini2:healthchecks-demo kalyan$ 
```

## Step-05: Limpeza
```bash
# Parar e remover containers
docker compose down -v

# Excluir imagens Docker
docker rmi $(docker images -q)
```