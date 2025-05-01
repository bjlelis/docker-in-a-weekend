---
title: Aprenda sobre o conceito de perfis no Docker Compose
description: Implemente o conceito de perfis no Docker Compose
---

## Step-01: Introdução
- Implemente o conceito de perfis no Docker Compose.

## Step-02: Revisar docker-compose.yaml
```yaml
  netshoot:
    image: nicolaka/netshoot
    container_name: ums-netshoot
    entrypoint: ["sleep", "infinity"]  # Mantém o container em execução para solução de problemas manual
    profiles: ["debug"]
    networks:
      - frontend
      - backend      
```

## Step-03: Iniciar a Pilha
```bash
# Baixar imagens Docker e iniciar os containers
docker compose up -d 

# Listar containers Docker
docker compose ps -a
Observação:
1. Todos os 3 containers serão criados.
2. Primeiro, "db-mysql" ficará saudável.
3. Segundo, "app-ums" ficará saudável.
4. Terceiro, "web-nginx" ficará saudável.
5. A inicialização ocorre sequencialmente: "db-mysql" -> "app-ums" -> "web-nginx".
6. O tráfego ao vivo será permitido apenas pelo nginx, e o nginx será iniciado somente após "db-mysql" e "app-ums" estarem saudáveis.

# Iniciar o serviço com o perfil 'debug'
docker compose --profile debug up -d

# Listar containers Docker
docker compose ps -a
docker ps -a
Observação:
1. O container "debug" será iniciado.

# Conectar ao container de debug
docker exec -it ums-netshoot /bin/bash

# Execute os seguintes comandos no container netshoot
## Teste de ping
ping web-nginx
ping app-ums
ping db-mysql

## Teste de telnet
telnet web-nginx 8080
telnet app-ums 8080
telnet db-mysql 3306

## Teste de dig
dig web-nginx
dig app-ums
dig db-mysql

## Teste de nslookup
nslookup web-nginx
nslookup app-ums
nslookup db-mysql

## Teste de curl
curl http://app-ums:8080/health
curl http://web-nginx:8080/health
```

## Step-04: Parar os Containers
```bash
# Parar e remover containers
docker compose down -v
Observação:
1. Apenas os containers de serviços regulares serão removidos (web-nginx, app-ums, db-mysql).
2. O container netshoot criado como parte do perfil '--profile' não será removido.
3. Precisamos removê-lo manualmente.

# Listar containers Docker
docker ps -a

# Listar redes Docker
docker network ls

# Parar e remover o serviço com o perfil 'debug'
docker compose --profile debug down
Observação:
1. O container netshoot será removido.

# Listar containers Docker
docker ps -a
Observação:
1. Nenhum container em execução ou parado.

# Listar redes Docker
docker network ls
Observação:
1. Nenhuma rede relacionada a esta pilha.
2. Tudo foi limpo.
```