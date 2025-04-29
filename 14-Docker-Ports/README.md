---
title: "Aprenda a Usar Portas de Containers Docker com Vários Flags"
description: "Entenda como usar portas de containers Docker com diferentes flags, incluindo '-p' e '-P', por meio de exemplos práticos."
---

# Aprenda a Usar Portas de Containers Docker com Vários Flags

---

## Introdução

Neste guia, você aprenderá a:

1. Usar portas de containers Docker com diferentes flags.
2. Entender a diferença entre os flags `-p` e `-P` ao executar containers Docker.
3. Publicar portas específicas do host e portas efêmeras.
4. Trabalhar com containers Docker de múltiplas portas.

---

## Demonstração 1: Entendendo Portas de Containers Docker com o Flag `-p`

### Passo 1: Criar Dockerfile e Arquivo Personalizado `index.html`

- **Diretório:** `DockerFiles`

**Crie um `Dockerfile`:**

```dockerfile
FROM nginx:alpine-slim
COPY index.html /usr/share/nginx/html
```

**Crie `index.html`:**

```html
<!DOCTYPE html> 
<html> 
  <body style='background-color:rgb(206, 141, 147);'> 
    <h1>Bem-vindo ao StackSimplify - Docker Ports HOST_PORT, CONTAINER_PORT</h1> 
    <p>Aprenda tecnologia por meio de demonstrações práticas e reais.</p> 
    <p>Versão da Aplicação: V1</p>     
  </body>
</html>
```

### Passo 2: Construir a Imagem Docker - Nginx Porta Única

```bash
# Mude para o diretório que contém seu Dockerfile
cd 01-DockerFiles-Single-Port

# Construa a Imagem Docker
docker build -t demo14-docker-singleport:v1 .

# Liste as Imagens Docker
docker images
```

### Passo 3: Publicar Porta Específica do Host

```bash
# Execute o Container Docker com uma porta específica do host
docker run --name my-ports-demo1 -p 8090:80 -d demo14-docker-singleport:v1

# Liste os Containers Docker
docker ps
docker ps --format "table {{.Image}}\t{{.Names}}\t{{.Status}}\t{{.ID}}\t{{.Ports}}"

# Acesse a aplicação no navegador
http://localhost:8090

# Acesse a aplicação usando curl
curl http://localhost:8090
```

**Observação:**

- A porta 80 do container está mapeada para a porta 8090 do host.
- Você pode acessar o servidor Nginx em `localhost:8090`.

### Passo 4: Publicar Portas Efêmeras

```bash
# Execute o Container Docker com uma porta efêmera do host
docker run --name my-ports-demo2 -p 80 -d demo14-docker-singleport:v1

# Liste os Containers Docker
docker ps
docker ps --format "table {{.Image}}\t{{.Names}}\t{{.Status}}\t{{.ID}}\t{{.Ports}}"

# Exemplo de Saída:
# IMAGE                       NAMES            STATUS         CONTAINER ID   PORTS
# demo14-docker-singleport:v1   my-ports-demo2   Up 10 seconds   abcdef123456   0.0.0.0:XXXXX->80/tcp

# Acesse a aplicação no navegador
http://localhost:XXXXX

# Acesse a aplicação usando curl
curl http://localhost:XXXXX
```

**Observação:**

- O Docker atribui uma porta efêmera aleatória no host, mapeada para a porta 80 do container.
- Substitua `XXXXX` pelo número da porta exibido no comando `docker ps`.

---

## Demonstração 2: Nginx Multi-Portas com o Flag `-P`

### Passo 1: Criar Dockerfile para Nginx Multi-Portas

- **Diretório:** `DockerFiles-Multi-Port`

**Crie um `Dockerfile`:**

```dockerfile
# Use nginx:alpine-slim como imagem base do Docker
FROM nginx:alpine-slim

# Defina variáveis de ambiente para configuração
ENV NGINX_PORT1=8080
ENV NGINX_PORT2=8081

# Labels OCI
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: Uso de Portas no Docker"
LABEL org.opencontainers.image.description="Um exemplo de Dockerfile ilustrando o uso de portas no Docker"
LABEL org.opencontainers.image.version="1.0"

# Labels Personalizados
LABEL nginx_port1=${NGINX_PORT1}
LABEL nginx_port2=${NGINX_PORT2}

# Instale o curl
RUN apk --no-cache add curl

# Crie diretórios para servir conteúdo
RUN mkdir -p /usr/share/nginx/html/app1 /usr/share/nginx/html/app2

# Copie o conteúdo para os diretórios respectivos
COPY app1/index.html /usr/share/nginx/html/app1
COPY app2/index.html /usr/share/nginx/html/app2
COPY index.html /usr/share/nginx/html

# Copie o arquivo de configuração personalizado do NGINX
COPY my_custom_nginx.conf /etc/nginx/conf.d/my_custom_nginx.conf

# Exponha as portas
EXPOSE $NGINX_PORT1 $NGINX_PORT2 80
```

### Passo 2: Criar Configuração Personalizada do Nginx

**Crie `my_custom_nginx.conf`:**

```conf
server {
    listen 8080;
    server_name localhost;

    location / {
        root /usr/share/nginx/html/app1;
        index index.html;
    }

    error_page 404 /404.html;
    location = /404.html {
        root /usr/share/nginx/html/app1;
    }
}

server {
    listen 8081;
    server_name localhost;

    location / {
        root /usr/share/nginx/html/app2;
        index index.html;
    }

    error_page 404 /404.html;
    location = /404.html {
        root /usr/share/nginx/html/app2;
    }
}
```

### Passo 3: Criar Arquivos Estáticos

**Crie `app1/index.html`:**

```html
<!DOCTYPE html> 
<html> 
  <body style='background-color:rgb(193, 136, 209);'> 
    <h1>Bem-vindo ao StackSimplify - MultiPort - App1 na Porta 8080</h1> 
    <p>Aprenda tecnologia por meio de demonstrações práticas e reais.</p> 
    <p>Versão da Aplicação: V1</p>     
  </body>
</html>
```

**Crie `app2/index.html`:**

```html
<!DOCTYPE html> 
<html> 
  <body style='background-color:rgb(136, 193, 209);'> 
    <h1>Bem-vindo ao StackSimplify - MultiPort - App2 na Porta 8081</h1> 
    <p>Aprenda tecnologia por meio de demonstrações práticas e reais.</p> 
    <p>Versão da Aplicação: V1</p>     
  </body>
</html>
```

**Crie `index.html`:**

```html
<!DOCTYPE html> 
<html> 
  <body style='background-color:rgb(209, 193, 136);'> 
    <h1>Bem-vindo ao StackSimplify - MultiPort - App3 na Porta 80 do Nginx default.conf</h1> 
    <p>Aprenda tecnologia por meio de demonstrações práticas e reais.</p> 
    <p>Versão da Aplicação: V1</p>     
  </body>
</html>
```

### Passo 4: Construir a Imagem Docker - Nginx Multi-Portas

```bash
# Mude para o diretório que contém seu Dockerfile
cd 02-DockerFiles-Multi-Port

# Construa a Imagem Docker
docker build -t demo14-docker-multiport:v1 .

# Liste as Imagens Docker
docker images
```

### Passo 5: Publicar Todas as Portas com o Flag `-P`

```bash
# Execute o Container Docker com todas as portas publicadas
docker run --name my-ports-demo3 -P -d demo14-docker-multiport:v1

# Liste os Containers Docker
docker ps
docker ps --format "table {{.Image}}\t{{.Names}}\t{{.Status}}\t{{.ID}}\t{{.Ports}}"

# Exemplo de Saída:
# IMAGE                       NAMES            STATUS         CONTAINER ID   PORTS
# demo14-docker-multiport:v1   my-ports-demo3   Up 10 seconds   abcdef123456   0.0.0.0:XXXXX->80/tcp, 0.0.0.0:YYYYY->8080/tcp, 0.0.0.0:ZZZZZ->8081/tcp

# Acesse as aplicações no navegador
http://localhost:XXXXX   # App3 na porta 80
http://localhost:YYYYY   # App1 na porta 8080
http://localhost:ZZZZZ   # App2 na porta 8081

# Acesse as aplicações usando curl
curl http://localhost:XXXXX
curl http://localhost:YYYYY
curl http://localhost:ZZZZZ
```

**Observação:**

- O flag `-P` publica todas as portas expostas para portas aleatórias no host.
- Substitua `XXXXX`, `YYYYY` e `ZZZZZ` pelos números das portas exibidos no comando `docker ps`.

---

## Conclusão

Você aprendeu a:

- Usar portas de containers Docker com diferentes flags.
- Utilizar o flag `-p` para mapear portas específicas do host e atribuir portas efêmeras.
- Utilizar o flag `-P` para publicar todas as portas expostas dinamicamente.
- Construir e executar imagens Docker para aplicações de porta única e múltiplas portas.
- Marcar e enviar imagens Docker para o Docker Hub.

---

**Feliz Dockerização!**