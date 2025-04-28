---
title: "Aprenda Dockerfile ADD com Fetch de URL na Prática"
description: "Aprenda a usar a instrução ADD em um Dockerfile para buscar conteúdo de uma URL, construir uma imagem Docker e enviá-la para o Docker Hub."
---

# Aprenda Dockerfile ADD com Fetch de URL na Prática

---

## Introdução

Neste guia, você irá:

- Criar um Dockerfile do Nginx usando `nginx:alpine-slim` como imagem base.
- Adicionar labels à sua imagem Docker.
- Usar a instrução `ADD` no Dockerfile para buscar conteúdo de uma URL (URL do GitHub).
- Construir a imagem Docker.
- Enviar a imagem Docker para o Docker Hub.

---

## Passo 1: Criar Repositório no GitHub e Fazer Upload de Arquivos

1. **Criar um Repositório no GitHub:**

   - Nome do Repositório: `docker-add-fetch-url-demo`
   - Tipo do Repositório: Público
   - Inicializar com um README (opcional).

2. **Fazer Upload de Arquivos:**

   - Faça upload da pasta `docs` para o seu repositório.
     - Você pode arrastar e soltar a pasta `docs` para facilitar o upload.

3. **Criar um Git Release:**

   - Vá para a seção **Releases** no seu repositório.
   - Clique em **Draft a new release**.
   - **Tag version:** `v1.0.0`
   - **Título do Release:** `Version 1.0.0`
   - Clique em **Publish release**.

---

## Passo 2: Criar Dockerfile e Adicionar Instruções

- **Diretório:** `Dockerfiles`

Crie um `Dockerfile` com o seguinte conteúdo:

```dockerfile
# Use nginx:alpine-slim como imagem base do Docker
FROM nginx:alpine-slim

# Labels OCI
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: Usando a Instrução ADD para Buscar Arquivos de uma URL no Dockerfile"
LABEL org.opencontainers.image.description="Um exemplo de Dockerfile ilustrando a instrução ADD, que demonstra como baixar e adicionar conteúdo de uma URL de Releases do GitHub ao container."
LABEL org.opencontainers.image.version="1.0"

# Usando Repositório do GitHub para baixar arquivos
ADD https://github.com/stacksimplify/docker-add-fetch-url-demo.git#v1.0.0:docs /usr/share/nginx/html
```

---

## Passo 3: Construir a Imagem Docker e Executá-la

```bash
# Mude para o diretório Dockerfiles
cd Dockerfiles

# Construa a imagem Docker
docker build -t [IMAGE-NAME]:[IMAGE-TAG] .

# Exemplo:
docker build -t demo6-dockerfile-add-fetch-url:v1 .

# Execute o container Docker e verifique
docker run --name my-add-fetch-url-demo -p 8080:80 -d demo6-dockerfile-add-fetch-url:v1

# Liste os arquivos estáticos no container Docker
docker exec -it my-add-fetch-url-demo ls -l /usr/share/nginx/html

# Acesse a aplicação
http://localhost:8080
```

---

## Passo 4: Parar e Remover Container e Imagens

```bash
# Pare e remova o container
docker rm -f my-add-fetch-url-demo

# Remova as imagens Docker
docker rmi [DOCKER_USERNAME]/[IMAGE-NAME]:[IMAGE-TAG]
docker rmi [IMAGE-NAME]:[IMAGE-TAG]

# Exemplo:
docker rmi demo6-dockerfile-add-fetch-url:v1

# Liste as imagens Docker para confirmar a remoção
docker images
```

---

## Conclusão

Você aprendeu a:

- Criar um Dockerfile usando `nginx:alpine-slim` como imagem base.
- Usar a instrução `ADD` para buscar conteúdo de uma URL (Release do GitHub).
- Construir e executar uma imagem Docker com conteúdo baixado diretamente do seu repositório GitHub.
- Enviar a imagem Docker para o Docker Hub.

---

## Notas Adicionais

- **Substitua os Marcadores:**

  - Lembre-se de substituir `[IMAGE-NAME]`, `[IMAGE-TAG]`, `[DOCKER_USERNAME]` pelos seus valores reais.

- **Usando `ADD` com URLs:**

  - A instrução `ADD` pode buscar arquivos de URLs remotas. No entanto, é geralmente recomendado usar `ADD` apenas para arquivos locais e usar `curl` ou `wget` em um comando `RUN` para buscar arquivos remotos, garantindo melhor controle e cache.

- **Considerações de Segurança:**

  - Tenha cuidado ao baixar arquivos de URLs externas, especialmente em builds automatizados, pois isso pode introduzir riscos de segurança.

- **Melhores Práticas:**

  - Limpe quaisquer arquivos temporários após a extração para reduzir o tamanho da imagem.
  - Use tags explícitas para suas imagens Docker para gerenciar versões de forma eficaz.

---

## Recursos Adicionais

- [Documentação do Docker](https://docs.docker.com/)
- [Referência do Dockerfile](https://docs.docker.com/engine/reference/builder/)
- [Melhores Práticas para Escrever Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Entendendo ADD vs. COPY no Dockerfile](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#add-or-copy)
- [Releases do GitHub](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)

---

**Feliz Dockerização!**