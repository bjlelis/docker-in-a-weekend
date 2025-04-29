---
title: "Aprenda as Instruções ARG no Dockerfile na Prática"
description: "Crie um Dockerfile com a instrução ARG para entender variáveis de tempo de build na construção de imagens Docker."
---

# Aprenda as Instruções ARG no Dockerfile na Prática

---

## Introdução

Neste guia, você irá:

- Criar um Dockerfile do Nginx usando `nginx:alpine-slim` como imagem base, com a versão do Nginx passada usando a instrução `ARG`.
- Construir imagens Docker usando o valor padrão definido no `Dockerfile` (`ARG NGINX_VERSION=1.26`).
- Construir imagens Docker substituindo a versão do Nginx durante o tempo de build usando `docker build --build-arg`.
- Executar os containers Docker e verificar as versões do Nginx.
- Realizar a limpeza.

---

## Passo 1: Criar Dockerfile com a Instrução ARG

- **Diretório:** `Dockerfiles`

Crie um `Dockerfile` com o seguinte conteúdo:

```dockerfile
# Defina um argumento de tempo de build para a versão do NGINX
ARG NGINX_VERSION=1.26

# Use nginx:alpine-slim como imagem base do Docker com a versão especificada do NGINX
FROM nginx:${NGINX_VERSION}-alpine-slim

# Labels OCI
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: Usando a Instrução ARG"
LABEL org.opencontainers.image.description="Um exemplo de Dockerfile ilustrando a instrução ARG"
LABEL org.opencontainers.image.version="1.0"

# Copie um arquivo index.html personalizado para o diretório HTML do Nginx
COPY index.html /usr/share/nginx/html
```

**Crie um arquivo simples `index.html`:**

```html
<!DOCTYPE html> 
<html> 
  <body style='background-color:rgb(227, 213, 180);'> 
    <h1>Bem-vindo ao StackSimplify - Variáveis de Tempo de Build ARG</h1> 
    <p>Aprenda tecnologia por meio de demonstrações práticas e reais.</p> 
    <p>Versão da Aplicação: V1</p>     
  </body>
</html>
```

---

## Passo 2: Construir Imagens Docker e Executá-las

### Construir Imagem Docker com Valor Padrão do ARG

```bash
# Mude para o diretório que contém seu Dockerfile
cd Dockerfiles

# Construa a imagem Docker usando o valor padrão NGINX_VERSION do Dockerfile
docker build -t [IMAGE-NAME]:[IMAGE-TAG] .

# Exemplo:
docker build -t demo7-dockerfile-arg:v1.26 .

# Execute o container Docker e verifique
docker run --name my-arg-demo1 -p 8080:80 -d demo7-dockerfile-arg:v1.26

# Verifique a versão do Nginx dentro do container
docker exec -it my-arg-demo1 nginx -v

# Acesse a aplicação no navegador
http://localhost:8080
```

**Saída Esperada:**

- A versão do Nginx deve ser **1.26**.
- A página personalizada do index deve ser exibida ao acessar [http://localhost:8080](http://localhost:8080).

### Construir Imagem Docker Substituindo o Valor do ARG

```bash
# Construa a imagem Docker especificando uma versão diferente do NGINX no tempo de build
docker build --build-arg NGINX_VERSION=1.27 -t [IMAGE-NAME]:[IMAGE-TAG] .

# Exemplo:
docker build --build-arg NGINX_VERSION=1.27 -t demo7-dockerfile-arg:v1.27 .

# Execute o container Docker e verifique
docker run --name my-arg-demo2 -p 8081:80 -d demo7-dockerfile-arg:v1.27

# Verifique a versão do Nginx dentro do container
docker exec -it my-arg-demo2 nginx -v

# Acesse a aplicação no navegador
http://localhost:8081
```

**Saída Esperada:**

- A versão do Nginx deve ser **1.27**.
- A página personalizada do index deve ser exibida ao acessar [http://localhost:8081](http://localhost:8081).

---

## Passo 3: Parar e Remover Containers e Imagens

```bash
# Pare e remova os containers
docker rm -f my-arg-demo1
docker rm -f my-arg-demo2

# Remova as imagens Docker da máquina local
docker rmi [DOCKER_USERNAME]/[IMAGE-NAME]:[IMAGE-TAG]
docker rmi [IMAGE-NAME]:[IMAGE-TAG]

# Exemplos:
docker rmi demo7-dockerfile-arg:v1.26
docker rmi demo7-dockerfile-arg:v1.27

# Liste as imagens Docker para confirmar a remoção
docker images
```

---

## Conclusão

Você aprendeu a:

- Criar um Dockerfile usando a instrução `ARG` para definir variáveis de tempo de build.
- Construir imagens Docker usando o valor padrão `ARG` especificado no Dockerfile.
- Substituir o valor do `ARG` durante o tempo de build usando `--build-arg` para especificar uma versão diferente do Nginx.
- Executar containers Docker e verificar as versões do Nginx.
- Marcar e enviar imagens Docker para o Docker Hub.

---

## Notas Adicionais

- **Substitua os Marcadores:** Lembre-se de substituir `[IMAGE-NAME]`, `[IMAGE-TAG]`, `[DOCKER_USERNAME]` e outros marcadores pelos seus valores reais.
- **Nome de Usuário do Docker Hub:** Certifique-se de estar logado com sua conta do Docker Hub ao enviar imagens.
- **ARG vs. ENV:**
  - Variáveis `ARG` estão disponíveis apenas durante o tempo de build da imagem.
  - Variáveis `ENV` estão disponíveis durante o tempo de execução dentro do container. Veremos isso no próximo exemplo (ARG e ENV combinados).
- **Melhores Práticas:**
  - Use tags explícitas para suas imagens Docker para gerenciar versões de forma eficaz.
  - Limpe imagens e containers não utilizados para liberar espaço em disco.

---

## Recursos Adicionais

- [Documentação do Docker](https://docs.docker.com/)
- [Referência do Dockerfile - Instrução ARG](https://docs.docker.com/engine/reference/builder/#arg)
- [Melhores Práticas para Escrever Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Entendendo ARG e ENV no Dockerfile](https://vsupalov.com/docker-arg-vs-env/)

---

**Feliz Dockerização!**