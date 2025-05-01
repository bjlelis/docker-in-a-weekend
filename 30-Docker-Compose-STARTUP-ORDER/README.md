---
title: Aprenda a implementar a ordem de inicialização usando depends_on no arquivo Docker Compose
description: Implemente a ordem de inicialização usando depends_on no arquivo Docker Compose
---

## Step-01: Introdução
- Implemente a ordem de inicialização usando depends_on no arquivo Docker Compose.

## Step-02: Revisar docker-compose.yaml
```yaml
# Para o Serviço: web-nginx
    depends_on:
      app-ums:
        condition: service_healthy
        restart: true   

# Para o Serviço: app-ums
    depends_on:
      db-mysql:
        condition: service_healthy
        restart: true        
```

## Step-03: Iniciar a Pilha
```bash
# Alterar para o diretório do projeto
cd startuporder-demo

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
```

## Step-04: Limpeza
```bash
# Parar e remover containers
docker compose down -v

# Excluir imagens Docker
docker rmi $(docker images -q)
```