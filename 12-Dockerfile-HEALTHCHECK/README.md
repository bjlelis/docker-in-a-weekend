---
title: "Aprenda a Instrução HEALTHCHECK no Dockerfile na Prática"
description: "Crie um Dockerfile com a instrução HEALTHCHECK para monitorar a saúde do container."
---

# Aprenda a Instrução HEALTHCHECK no Dockerfile na Prática

---

## Introdução

Neste guia, você irá:

- Criar um Dockerfile do Nginx usando `nginx:alpine-slim` como imagem base.
- Implementar uma verificação de saúde usando a instrução `HEALTHCHECK`.
- Construir a imagem Docker e verificar sua funcionalidade.

---

## Passo 1: Criar Dockerfile e Arquivo Personalizado `index.html`

- **Referência da Instrução HEALTHCHECK no Dockerfile:** [Instrução HEALTHCHECK no Dockerfile](https://docs.docker.com/engine/reference/builder/#healthcheck)

- **Diretório:** `DockerFiles`

**Crie um `Dockerfile` com o seguinte conteúdo:**

```dockerfile
# Use nginx:alpine-slim como imagem base do Docker
FROM nginx:alpine-slim

# Labels OCI
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: Instrução HEALTHCHECK no Docker"
LABEL org.opencontainers.image.description="Um exemplo de Dockerfile ilustrando o uso da instrução HEALTHCHECK"
LABEL org.opencontainers.image.version="1.0"

# Instale o curl (necessário para o comando de verificação de saúde)
RUN apk --no-cache add curl

# Usando COPY para copiar um arquivo local
COPY index.html /usr/share/nginx/html

# A instrução HEALTHCHECK informa ao Docker como testar um container para verificar se ele ainda está funcionando
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --start-interval=5s --retries=3 CMD curl -f http://localhost/ || exit 1
```

**Crie um arquivo personalizado `index.html`:**

```html
<!DOCTYPE html> 
<html> 
  <body style='background-color:rgb(227, 213, 180);'> 
    <h1>Bem-vindo ao StackSimplify - Instrução HEALTHCHECK no Dockerfile</h1> 
    <p>Aprenda tecnologia por meio de demonstrações práticas e reais.</p> 
    <p>Versão da Aplicação: V1</p>     
  </body>
</html>
```

---

## Passo 2: Construir a Imagem Docker e Executá-la

```bash
# Mude para o diretório que contém seu Dockerfile
cd DockerFiles

# Construa a imagem Docker
docker build -t demo12-dockerfile-healthcheck:v1 .

# Inspecione a imagem Docker
docker image inspect demo12-dockerfile-healthcheck:v1

# Inspecione as configurações de Healthcheck da imagem Docker
docker image inspect --format='{{json .Config.Healthcheck}}' demo12-dockerfile-healthcheck:v1

# Execute o container Docker
docker run --name my-healthcheck-demo -p 8080:80 -d demo12-dockerfile-healthcheck:v1

# Liste os containers Docker
docker ps

# Saída Esperada:
# CONTAINER ID   IMAGE                             COMMAND                  CREATED          STATUS                    PORTS                  NAMES
# e63e7fe79986   demo12-dockerfile-healthcheck:v1  "/docker-entrypoint.…"   17 seconds ago   Up 15 seconds (healthy)   0.0.0.0:8080->80/tcp   my-healthcheck-demo

# Inspecione o status de saúde do container
docker inspect --format='{{json .State.Health}}' my-healthcheck-demo

# Acesse a aplicação no navegador
http://localhost:8080
```

**Observações:**

1. O container deve estar em estado **healthy** conforme indicado pela coluna `STATUS` no comando `docker ps`.
2. A instrução `HEALTHCHECK` verifica periodicamente a saúde da aplicação dentro do container.

---

## Passo 3: Parar e Remover Container e Imagens

```bash
# Pare e remova o container
docker rm -f my-healthcheck-demo

# Remova as imagens Docker da máquina local
docker rmi stacksimplify/demo12-dockerfile-healthcheck:v1
docker rmi demo12-dockerfile-healthcheck:v1

# Liste as imagens Docker para confirmar a remoção
docker images
```

---

## Conclusão

Você aprendeu a:

- Criar um Dockerfile do Nginx usando a instrução `HEALTHCHECK`.
- Construir a imagem Docker e executá-la, observando o status de saúde.
- Verificar a funcionalidade de verificação de saúde do container.
- Marcar e enviar a imagem Docker para o Docker Hub.

---

## Notas Adicionais

- **Instrução HEALTHCHECK:**

  - A instrução `HEALTHCHECK` informa ao Docker como testar um container para verificar se ele ainda está funcionando.
  - É útil para monitorar a saúde da aplicação em execução dentro do container.
  - **Sintaxe:**

    ```dockerfile
    HEALTHCHECK [OPTIONS] CMD comando
    ```

  - **Opções:**
    - `--interval=` (padrão: `30s`): Tempo entre as verificações.
    - `--timeout=` (padrão: `30s`): Tempo permitido para a verificação antes de ser considerada como falha.
    - `--start-period=` (padrão: `0s`): Tempo de inicialização antes de começar as verificações de saúde.
    - `--retries=` (padrão: `3`): Número de falhas consecutivas necessárias para considerar o container como não saudável.

- **Observações:**

  - O status de saúde pode ser `starting`, `healthy` ou `unhealthy`.
  - Use `docker inspect` para obter informações detalhadas sobre o status de saúde.

---

## Recursos Adicionais

- [Documentação do Docker](https://docs.docker.com/)
- [Referência do Dockerfile - Instrução HEALTHCHECK](https://docs.docker.com/engine/reference/builder/#healthcheck)
- [Melhores Práticas para Escrever Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Monitorando a Saúde de Containers](https://docs.docker.com/config/containers/healthcheck/)

---

**Feliz Dockerização!**