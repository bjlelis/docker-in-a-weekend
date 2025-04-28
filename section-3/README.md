---
title: "How to Create and Push Docker Images to Docker Hub: A Step-by-Step Guide"
description: "Learn how to build a Docker image, tag it, and push it to Docker Hub. This tutorial covers creating a Docker Hub account, Dockerfile creation, image building, tagging, and pushing to Docker Hub."
---

# How to Create and Push Docker Images to Docker Hub: A Step-by-Step Guide

---

## Introdução

Neste guia iremos:

1. Criar Docker Hub account.
2. logar com  Docker ID em um Docker Desktop.
3. Logar no Docker Hub usando Docker CLI.
4. Run em base Nginx Docker image.
5. Criar um custom `Dockerfile` e `index.html`.
6. Build de Docker image a partir do `Dockerfile`.
7. Tag e push da image para o Docker Hub.
8. Explorar Docker images no Docker Hub.

---

## Step 1: Create Docker Hub Account

- Visite https://hub.docker.com/ e crie uma conta.
---

## Step 2: Rodar um Base Nginx Container

- Refer to the [NGINX Docker Image on Docker Hub](https://hub.docker.com/_/nginx).

```
# Run no Nginx Docker Image
docker run --name <CONTAINER-NAME> -p <HOST_PORT>:<CONTAINER_PORT> -d <IMAGE_NAME>:<TAG>

# Listar running containers
docker ps

# Acessar a aplicação no browser
http://localhost:8090

# Stop e remova o Docker container
docker stop myapp1
docker rm myapp1

# Ou force remove no container
docker rm -f myapp1
```

---

# Step 3: Criar o Dockerfile e Customizar o `index.html`

- **Directory:** `Dockerfiles`

**Criar o `Dockerfile`:**

```dockerfile
FROM nginx
COPY index.html /usr/share/nginx/html
```

**Criar o `index.html`:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>StackSimplify</title>
  <style>
    body { 
      font-family: Arial, sans-serif; 
      text-align: center; 
      padding: 50px; 
      background-color: rgb(197, 144, 144);
    }
    h1 { font-size: 50px; }
    h2 { font-size: 40px; }
    h3 { font-size: 30px; }
    p { font-size: 20px; }
  </style>
</head>
<body>
  <h1>Welcome to StackSimplify</h1>
  <h2>Docker Image BUILD, RUN, TAG and PUSH to Docker Hub</h2>
  <p>Learn technology through practical, real-world demos.</p>
  <p>Application Version: v1</p>
</body>
</html>
```

---

## Step 4: Build da Imagem e o Run

```
# Vá para o diretório do Dockerfile
cd Dockerfiles

# Build image
docker build -t <IMAGE_NAME>:<TAG> .

# Rodar o container com a imagem
docker run --name <CONTAINER-NAME> -p <HOST_PORT>:<CONTAINER_PORT> -d <IMAGE_NAME>:<TAG>

# Exemplo:
docker run --name mynginx1 -p 8090:80 -d mynginx-custom:v1

# Acesse no your browser
http://localhost:8090
```

---

## Step 5: Tag e Push da Image para o Docker Hub

```
# Listar Docker images
docker images

# Tag na image
docker tag mynginx-custom:v1 YOUR_DOCKER_USERNAME/mynginx-custom:v1

# Exemplo 'stacksimplify':
docker tag mynginx-custom:v1 stacksimplify/mynginx-custom:v1

# Push da image para o Docker Hub
docker push YOUR_DOCKER_USERNAME/mynginx-custom:v1

# Example with 'stacksimplify':
docker push stacksimplify/mynginx-custom:v1
USERNAME with your actual Docker Hub username.

```

---

## Step 8: Verificar a imagem no docker hub

- Logar n Docker Hub e verificar se ela está lá.
- Navegue nos seus repositorios (https://hub.docker.com/repositories).

---

## Step 10: Use o docker search comando na CLI

```
# SProcure por 'nginx' images
docker search nginx

# Limite resultados para 5
docker search nginx --limit 5

# Filtrar por stars:
docker search --filter=stars=50 nginx

# Filtrar por imagens oficiais:
docker search --filter=is-official=true nginx
```
