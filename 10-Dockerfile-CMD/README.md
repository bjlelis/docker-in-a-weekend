---
title: "Aprenda as Instruções CMD no Dockerfile na Prática"
description: "Entenda como usar a instrução CMD em Dockerfiles e como sobrescrever CMD durante o comando 'docker run'."
---

# Aprenda as Instruções CMD no Dockerfile na Prática

---

## Introdução

Neste guia, você irá:

- Criar um Dockerfile do Nginx com a instrução `CMD`.
- Entender como sobrescrever a instrução `CMD` durante o comando `docker run`.
- Construir a imagem Docker e verificar sua funcionalidade.

---

## Passo 1: Criar Dockerfile e Arquivo Personalizado `index.html`

- **Diretório:** `DockerFiles`

**Crie um `Dockerfile` com o seguinte conteúdo:**

```dockerfile
# Use nginx:alpine-slim como imagem base do Docker
FROM nginx:alpine-slim

# Labels OCI
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: CMD Instruction in Docker"
LABEL org.opencontainers.image.description="Um exemplo de Dockerfile ilustrando o uso da instrução CMD"
LABEL org.opencontainers.image.version="1.0"

# Copie um arquivo index.html personalizado para o diretório HTML do Nginx
COPY index.html /usr/share/nginx/html

# CMD padrão para iniciar o Nginx em primeiro plano
CMD ["nginx", "-g", "daemon off;"]
```

**Crie um arquivo simples `index.html`:**

```html
<!DOCTYPE html> 
<html> 
  <body style='background-color:rgb(227, 213, 180);'> 
    <h1>Bem-vindo ao StackSimplify - Instrução CMD no Dockerfile</h1> 
    <p>Aprenda tecnologia por meio de demonstrações práticas e reais.</p> 
    <p>Versão da Aplicação: V1</p>     
    <p>CMD: Especifica comandos padrão.</p>     
  </body>
</html>
```

---

## Passo 2: Construir a Imagem Docker e Executá-la

```bash
# Mude para o diretório que contém seu Dockerfile
cd DockerFiles

# Construa a imagem Docker
docker build -t [IMAGE_NAME]:[TAG] .

# Exemplo:
docker build -t demo10-dockerfile-cmd:v1 .

# Execute o container Docker
docker run --name my-cmd-demo1 -p 8080:80 -d demo10-dockerfile-cmd:v1

# Verifique se o Nginx está em execução dentro do container
docker exec -it my-cmd-demo1 ps aux

# Saída Esperada:
# Você deve ver o processo Nginx em execução com 'nginx: master process nginx -g daemon off;'

# Acesse a aplicação no navegador
http://localhost:8080
```

**Observações:**

1. O processo Nginx deve estar em execução dentro do container.
2. O comando `CMD ["nginx", "-g", "daemon off;"]` definido no Dockerfile é executado como está.

---

## Passo 3: Executar o Container Docker Sobrescrevendo CMD

```bash
# Execute o container Docker sobrescrevendo a instrução CMD
docker run --name my-cmd-demo2 -it demo10-dockerfile-cmd:v1 /bin/sh

# Execute dentro do container o comando ps aux
ps aux

# Saída Esperada:
# O Nginx não está em execução porque o CMD foi sobrescrito com '/bin/sh'

# Você pode iniciar o Nginx manualmente, se desejar:
nginx -g 'daemon off;'

# Para sair do shell do container:
exit
```

**Observações:**

1. Após conectar-se ao container Docker, o Nginx não estará em execução.
2. A instrução `CMD` foi sobrescrita com `/bin/sh` durante o comando `docker run`.

---

## Passo 4: Parar e Remover Containers e Imagens

```bash
# Pare e remova os containers
docker rm -f my-cmd-demo1
docker rm -f my-cmd-demo2

# Remova as imagens Docker da máquina local
docker rmi [DOCKER_USERNAME]/[IMAGE_NAME]:[TAG]
docker rmi [IMAGE_NAME]:[TAG]

# Exemplo:
docker rmi demo10-dockerfile-cmd:v1

# Liste as imagens Docker para confirmar a remoção
docker images
```

---

## Conclusão

Você aprendeu a:

- Criar um Dockerfile do Nginx usando a instrução `CMD`.
- Construir a imagem Docker e executá-la, observando a execução padrão do `CMD`.
- Sobrescrever a instrução `CMD` durante o comando `docker run` e verificar seu efeito.
- Marcar e enviar a imagem Docker para o Docker Hub.

---

## Notas Adicionais

- **Instrução CMD:**

  - A instrução `CMD` especifica o comando padrão a ser executado ao iniciar um container a partir da imagem.
  - Pode ser sobrescrita especificando um comando diferente durante o `docker run`.
  - Apenas a última instrução `CMD` no Dockerfile tem efeito.

- **Sobrescrevendo CMD:**

  - Quando você especifica um comando no final do comando `docker run`, ele sobrescreve o `CMD` especificado no Dockerfile.
  - Isso é útil quando você deseja executar comandos diferentes usando a mesma imagem.

- **Melhores Práticas:**

  - Use `CMD` para especificar o comando padrão para o container.
  - Use `ENTRYPOINT` quando quiser definir um comando fixo e permitir parâmetros adicionais.
  - Evite usar `ENTRYPOINT` e `CMD` juntos, a menos que seja necessário.

---

## Recursos Adicionais

- [Documentação do Docker](https://docs.docker.com/)
- [Referência do Dockerfile - Instrução CMD](https://docs.docker.com/engine/reference/builder/#cmd)
- [Melhores Práticas para Escrever Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Entendendo CMD e ENTRYPOINT no Docker](https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact)

---

**Feliz Dockerização!**