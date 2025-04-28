---
title: "Criar Imagem Docker com Labels e Enviar para o Docker Hub"
description: "Aprenda a criar uma imagem Docker com labels, construí-la, inspecioná-la e enviá-la para o Docker Hub. Este guia cobre a criação do Dockerfile, adição de labels, construção de imagens e uso do comando docker inspect."
---

# Criar Imagem Docker com Labels e Enviar para o Docker Hub

---

## Introdução

Neste guia, você irá:

- Criar um Dockerfile do Nginx usando `nginx:alpine-slim` como imagem base.
- Adicionar labels à sua imagem Docker.
- Criar um arquivo simples `index.html`.
- Construir a imagem Docker.
- Enviar a imagem Docker para o Docker Hub.
- Aprender sobre o comando `docker inspect`.

---

## Passo 1: Criar Dockerfile e Arquivo `index.html` Personalizado

- **Imagem Base:** [Nginx Alpine Slim](https://hub.docker.com/_/nginx/tags?page_size=&ordering=&name=alpine-slim)
- **Diretório:** `Dockerfiles`

**Crie um `Dockerfile`:**

```dockerfile
# Use nginx:alpine-slim como imagem base do Docker
FROM nginx:alpine-slim

# Labels personalizados
LABEL maintainer="Kalyan Reddy Daida"  
LABEL version="1.0"
LABEL description="Uma aplicação simples do Nginx"
# Labels OCI
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Aplicação Nginx Alpine Slim"
LABEL org.opencontainers.image.description="Uma aplicação leve do Nginx construída no Alpine."
LABEL org.opencontainers.image.version="1.0"
LABEL org.opencontainers.image.revision="1234567890abcdef" 
LABEL org.opencontainers.image.created="2024-10-14T08:30:00Z"
LABEL org.opencontainers.image.url="https://github.com/stacksimplify/docker-in-a-weekend"
LABEL org.opencontainers.image.source="https://github.com/stacksimplify/docker-in-a-weekend/tree/main/04-Dockerfile-LABELS/Dockerfiles"
LABEL org.opencontainers.image.documentation="https://github.com/stacksimplify/docker-in-a-weekend/tree/main/04-Dockerfile-LABELS"
LABEL org.opencontainers.image.vendor="STACKSIMPLIFY"
LABEL org.opencontainers.image.licenses="Apache-2.0"

# Usando COPY para copiar um arquivo local
COPY index.html /usr/share/nginx/html
```

**Crie um arquivo simples `index.html`:**

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
      background-color: rgb(227, 213, 180);
    }
    h1 { font-size: 50px; }
    h2 { font-size: 40px; }
    h3 { font-size: 30px; }
    p { font-size: 20px; }
  </style>
</head>
<body>
  <h1>Welcome to StackSimplify</h1>
  <h2>Dockerfile: Nginx Alpine Slim Docker Image with custom LABELS and OCI LABELS</h2>
  <p>Learn technology through practical, real-world demos.</p>
  <p>Application Version: v1</p>
</body>
</html>
```

---

## Passo 2: Construir a Imagem Docker e Executá-la

```bash
# Mude para o diretório que contém seu Dockerfile
cd Dockerfiles

# Construa a imagem Docker
docker build -t [IMAGE-NAME]:[IMAGE-TAG] .

# Exemplo:
docker build -t demo4-dockerfile-labels:v1 .

# Notas Importantes:
# 1. [IMAGE-TAG] é opcional; se não fornecido, o padrão será "latest".
# 2. A melhor prática é usar tags explícitas.

# Liste as imagens Docker
docker images

# Execute o container Docker
docker run --name mylabels-demo -p 8080:80 -d demo4-dockerfile-labels:v1

# Acesse a aplicação no navegador
http://localhost:8080
```

---

## Passo 3: Instalar o Pacote `jq`

`jq` é um processador de JSON leve e flexível para linha de comando, útil para analisar a saída JSON de comandos como `docker inspect`.

**Para macOS:**

```bash
brew install jq
jq --version
```

**Para Linux (Ubuntu/Debian):**

```bash
sudo apt-get update
sudo apt-get install jq
jq --version
```

**Para Linux (CentOS/RHEL):**

```bash
sudo yum install epel-release
sudo yum install jq
jq --version
```

**Para Linux (Fedora):**

```bash
sudo dnf install jq
jq --version
```

**Para Outras Distribuições Linux:**

```bash
wget -O jq https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64
chmod +x ./jq
sudo mv jq /usr/local/bin
jq --version
```

**Para Windows (Usando Chocolatey):**

```bash
choco install jq
jq --version
```

**Para Windows (Instalação Manual):**

1. Baixe o executável de [jq Releases](https://github.com/stedolan/jq/releases).
2. Escolha `jq-win64.exe` (ou `jq-win32.exe` para sistemas 32-bit).
3. Renomeie o arquivo baixado para `jq.exe`.
4. Mova-o para uma pasta no PATH do sistema (ex.: `C:\Windows`).

---

## Passo 4: Comandos de Inspeção de Imagem Docker

Use `docker inspect` para obter informações detalhadas sobre imagens Docker.

```bash
# Inspecione a imagem Docker
docker image inspect [IMAGE-NAME]:[IMAGE-TAG]

# Exemplo:
docker image inspect demo4-dockerfile-labels:v1

# Obtenha a data de criação da imagem Docker
docker inspect --format='{{.Created}}' [IMAGE-NAME]:[IMAGE-TAG]

# Exemplo:
docker inspect --format='{{.Created}}' demo4-dockerfile-labels:v1

# Obtenha os labels da imagem Docker (não formatado)
docker inspect --format='{{json .Config.Labels}}' [IMAGE-NAME]:[IMAGE-TAG]

# Exemplo:
docker image inspect --format='{{json .Config.Labels}}' demo4-dockerfile-labels:v1

# Obtenha os labels da imagem Docker (formatado com jq)
docker image inspect --format='{{json .Config.Labels}}' [IMAGE-NAME]:[IMAGE-TAG] | jq

# Exemplo:
docker image inspect --format='{{json .Config.Labels}}' demo4-dockerfile-labels:v1 | jq
```

---

## Passo 5: Comandos de Inspeção de Container Docker

Use `docker inspect` para obter informações detalhadas sobre containers Docker.

```bash
# Inspecione o container Docker
docker inspect [CONTAINER-NAME or CONTAINER-ID]

# Exemplo:
docker inspect mylabels-demo

# Obtenha o endereço IP do container
docker inspect --format='{{.NetworkSettings.IPAddress}}' [CONTAINER-NAME or CONTAINER-ID]

# Exemplo:
docker inspect --format='{{.NetworkSettings.IPAddress}}' mylabels-demo

# Inspecione o estado do container (executando, pausado, parado)
docker inspect --format='{{.State.Status}}' [CONTAINER-NAME or CONTAINER-ID]

# Exemplo:
docker inspect --format='{{.State.Status}}' mylabels-demo

# Inspecione as portas expostas
docker inspect --format='{{json .Config.ExposedPorts}}' [CONTAINER-NAME or CONTAINER-ID]

# Exemplo:
docker inspect --format='{{json .Config.ExposedPorts}}' mylabels-demo

# Inspecione os detalhes de rede do container (formatado com jq)
docker inspect --format='{{json .NetworkSettings}}' [CONTAINER-NAME or CONTAINER-ID] | jq

# Exemplo:
docker inspect --format='{{json .NetworkSettings}}' mylabels-demo | jq
```

---

## Passo 6: Parar e Remover Container e Imagens

```bash
# Pare e remova o container
docker rm -f mylabels-demo

# Remova as imagens Docker
docker rmi demo4-dockerfile-labels:v1

# Liste as imagens Docker para confirmar a remoção
docker images
```

---

## Conclusão

Você aprendeu a:

- Criar um Dockerfile com labels usando `nginx:alpine-slim` como imagem base.
- Construir e executar uma imagem Docker com labels personalizados.
- Enviar a imagem Docker para o Docker Hub.
- Usar o comando `docker inspect` para obter informações detalhadas sobre imagens e containers.
- Instalar e usar o `jq` para formatar a saída JSON de comandos Docker.

---

## Notas Adicionais

- **Substitua os Marcadores:** Lembre-se de substituir `[IMAGE-NAME]`, `[IMAGE-TAG]`, `[DOCKER_USERNAME]`, `[CONTAINER-NAME]` e outros marcadores pelos seus valores reais.
- **Usuário do Docker Hub:** Certifique-se de estar logado com sua conta do Docker Hub ao enviar imagens.
- **Labels:** Labels são pares chave-valor que permitem adicionar metadados às suas imagens Docker. Eles seguem a [Especificação de Formato de Imagem OCI](https://github.com/opencontainers/image-spec/blob/master/annotations.md).
- **Uso do `jq`:** A ferramenta `jq` é usada para analisar a saída JSON, facilitando a leitura e extração de informações específicas de comandos como `docker inspect`.

---

## Recursos Adicionais

- [Documentação do Docker](https://docs.docker.com/)
- [Referência do Dockerfile](https://docs.docker.com/engine/reference/builder/)
- [Melhores Práticas para Escrever Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Comando Docker Inspect](https://docs.docker.com/engine/reference/commandline/inspect/)
- [Especificação de Formato de Imagem OCI](https://github.com/opencontainers/image-spec/blob/master/annotations.md)
- [Manual do jq](https://stedolan.github.io/jq/manual/)

---

**Feliz Dockerização!**