---
title: "Crie Imagens Docker Multi-Plataforma Usando BuildKit e Buildx"
description: "Aprenda a criar e enviar imagens Docker multi-plataforma usando Docker BuildKit e Buildx. Este guia aborda o uso das flags `--load` e `--push` com o comando `docker buildx build` para criação eficiente de imagens multi-arquitetura."
---

# Crie Imagens Docker Multi-Plataforma Usando BuildKit e Buildx

---

## Step-01: Introdução

Neste guia, você aprenderá a criar imagens Docker multi-plataforma usando **Docker BuildKit** e **Buildx**. Também aprenderá a usar as flags `--load` e `--push` com o comando `docker buildx build`.

---

## Step-02: Revisar o Dockerfile

```dockerfile
# Usar nginx como imagem base do Docker
FROM nginx

# Labels OCI
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: Criação de Imagens Docker Multi-Plataforma usando Docker BuildKit e Buildx"
LABEL org.opencontainers.image.description="Um exemplo de Dockerfile ilustrando Imagens Docker Multi-Plataforma usando Docker BuildKit e Buildx"
LABEL org.opencontainers.image.version="1.0"

# Usar COPY para copiar um arquivo local
COPY index.html /usr/share/nginx/html
```

---

## Step-03: Verificar Suporte Multi-Plataforma da Imagem Base do NGINX

- Verifique a [Imagem Oficial do NGINX no Docker Hub](https://hub.docker.com/_/nginx) para confirmar se ela suporta múltiplas plataformas.
- Na seção **Quick reference (cont.)**, você encontrará as arquiteturas suportadas:

```text
Arquiteturas suportadas:
amd64, arm32v5, arm32v6, arm32v7, arm64v8, i386, mips64le, ppc64le, s390x
```

---

## Step-04: Construir e Carregar Imagens Docker Multi-Plataforma Localmente

```bash
# Listar builders locais
docker buildx ls

# Alterar para o diretório do projeto
cd multiplatform-demo

# Construir imagens Docker multi-plataforma e carregar no Docker Desktop (localmente)
docker buildx build --platform linux/amd64,linux/arm64 -t demo1-multiplatform-local:v1 --load .
```

- **Nota**:
  - Ao construir imagens multi-plataforma, é recomendado usar `--push` em vez de `--load`.
  - A flag `--load` é útil para desenvolvimento local, mas suporta apenas uma plataforma por vez no daemon Docker local.

---

## Step-05: Construir e Enviar Imagens Docker Multi-Plataforma para o Docker Hub

```bash
# Listar builders locais
docker buildx ls

# Fazer login com seu Docker ID
docker login

# Alterar para o diretório do projeto
cd multiplatform-demo

# Construir imagens Docker multi-plataforma e enviar para o Docker Hub
docker buildx build --platform linux/amd64,linux/arm64 -t SEU_DOCKER_ID/demo2-multiplatform-local:v1 --push .
docker buildx build --platform linux/amd64,linux/arm64 -t stacksimplify/demo2-multiplatform-local:v1 --push .
```

- **Substitua** `SEU_DOCKER_ID` pelo seu nome de usuário no Docker Hub.

---

## Step-06: Verificar Imagem Docker Multi-Plataforma no Docker Hub

1. Acesse [Docker Hub](https://hub.docker.com).
2. Navegue até sua imagem Docker: `SEU_DOCKER_ID/demo2-multiplatform-local`.
3. Clique em **Tags**.
4. Verifique se há múltiplos digests de imagem correspondentes a diferentes arquiteturas (por exemplo, arm64 e amd64).

---

## Step-07: Baixar, Executar e Verificar a Imagem Docker

```bash
# Baixar a imagem Docker
docker pull SEU_DOCKER_ID/demo2-multiplatform-local:v1
docker pull stacksimplify/demo2-multiplatform-local:v1

# Inspecionar a imagem Docker
docker image inspect SEU_DOCKER_ID/demo2-multiplatform-local:v1
docker image inspect stacksimplify/demo2-multiplatform-local:v1

# Observação:
# 1. Verifique o campo "Architecture" na saída.
# 2. A imagem baixada corresponde à arquitetura da sua máquina local.

# Executar o container Docker
docker run --name my-multiplatform-demo -p 8080:80 -d SEU_DOCKER_ID/demo2-multiplatform-local:v1
docker run --name my-multiplatform-demo -p 8080:80 -d stacksimplify/demo2-multiplatform-local:v1

# Listar containers Docker
docker ps

# Acessar a aplicação
# No navegador:
http://localhost:8080

# Ou use curl:
curl http://localhost:8080
```

- **Limpeza**:

```bash
# Parar o container Docker
docker stop my-multiplatform-demo

# Remover o container Docker
docker rm my-multiplatform-demo
```

---

## Step-08: Parar e Remover o Builder Buildx

```bash
# Listar builders do Docker Buildx
docker buildx ls

# Parar o builder Buildx
docker buildx stop mybuilder1

# Remover o builder Buildx
docker buildx rm mybuilder1

# Verificar os builders
docker buildx ls
```

---

## Step-09: Limpeza

```bash
# Remover todas as imagens Docker
docker rmi $(docker images -q)

# Listar imagens Docker para confirmar
docker images
```

---

## Conclusão

Neste tutorial, você aprendeu a criar imagens Docker multi-plataforma usando Docker BuildKit e Buildx. Ao aproveitar o comando `docker buildx build` com as flags `--platform`, `--load` e `--push`, você pode criar imagens que suportam múltiplas arquiteturas e enviá-las para o Docker Hub para maior compatibilidade.

---

## Notas Adicionais

- **Imagens Multi-Plataforma**:
  - Imagens multi-plataforma (também conhecidas como imagens multi-arquitetura) permitem criar imagens que podem ser executadas em diferentes arquiteturas de CPU, como `amd64` e `arm64`.
  - Isso é particularmente útil para suportar vários dispositivos e ambientes.

- **Buildx e BuildKit**:
  - **Buildx** é um plugin CLI que estende o comando `docker build` com suporte completo aos recursos fornecidos pelo toolkit BuildKit.
  - **BuildKit** oferece desempenho aprimorado e novos recursos para builds de imagens Docker.

- **Usando `--push` vs. `--load`**:
  - `--push`: Constrói a imagem e a envia diretamente para um registro Docker. Recomendado para imagens multi-plataforma.
  - `--load`: Carrega a imagem no armazenamento de imagens Docker local. Suporta apenas a plataforma atual.

---

## Recursos Adicionais

- [Documentação do Docker Buildx](https://docs.docker.com/buildx/working-with-buildx/)
- [Documentação do Docker BuildKit](https://docs.docker.com/build/buildkit/)
- [Builds Docker Multi-Plataforma](https://www.docker.com/blog/multi-arch-build-and-images-the-simple-way/)
- [Imagem Oficial do NGINX no Docker Hub](https://hub.docker.com/_/nginx)
- [Referência do Comando Docker Buildx Build](https://docs.docker.com/engine/reference/commandline/buildx_build/)

---

**Feliz Dockerização!**