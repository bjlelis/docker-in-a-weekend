---
title: "Aprenda as Instruções ENTRYPOINT no Dockerfile na Prática"
description: "Entenda como usar a instrução ENTRYPOINT em Dockerfiles e como sobrescrever ou adicionar argumentos durante o comando 'docker run'."
---

# Aprenda as Instruções ENTRYPOINT no Dockerfile na Prática

---

## Introdução

Neste guia, você irá:

- Criar um Dockerfile com a instrução `ENTRYPOINT`.
- Construir uma imagem Docker e verificar sua funcionalidade.
- Entender como:
  - Usar `ENTRYPOINT` conforme definido no Dockerfile.
  - Adicionar argumentos adicionais à instrução `ENTRYPOINT`.
  - Sobrescrever a instrução `ENTRYPOINT` usando a flag `--entrypoint`.

---

## Passo 1: Criar Dockerfile

- **Diretório:** `DockerFiles`

Crie um `Dockerfile` com o seguinte conteúdo:

```dockerfile
# Use ubuntu como imagem base do Docker
FROM ubuntu

# Labels OCI
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: Instrução ENTRYPOINT no Docker"
LABEL org.opencontainers.image.description="Um exemplo de Dockerfile ilustrando o uso da instrução ENTRYPOINT"
LABEL org.opencontainers.image.version="1.0"

# Sempre execute o comando echo como entrypoint
ENTRYPOINT ["echo", "Kalyan"]
```

---

## Passo 2: Construir a Imagem Docker e Executá-la

### Construir a Imagem Docker

```bash
# Mude para o diretório que contém seu Dockerfile
cd DockerFiles

# Construa a imagem Docker
docker build -t demo11-dockerfile-entrypoint:v1 .
```

### Demonstração 1: Usar ENTRYPOINT Como Está

```bash
# Execute o container Docker e verifique
docker run --name my-entrypoint-demo1 demo11-dockerfile-entrypoint:v1

# Saída Esperada:
# Kalyan
```

**Observação:**

- O container é executado e exibe `Kalyan`, que é o argumento fornecido na instrução `ENTRYPOINT` durante a construção da imagem Docker.

### Demonstração 2: Adicionar Argumentos à ENTRYPOINT

```bash
# Execute o container Docker e adicione um argumento adicional
docker run --name my-entrypoint-demo2 demo11-dockerfile-entrypoint:v1 Reddy

# Saída Esperada:
# Kalyan Reddy
```

**Observação:**

- O argumento adicional `Reddy` é adicionado à instrução `ENTRYPOINT`.
- O container exibe `Kalyan Reddy`.

### Demonstração 3: Sobrescrever a Instrução ENTRYPOINT

```bash
# Execute o container Docker e sobrescreva a instrução ENTRYPOINT
docker run --name my-entrypoint-demo3 --entrypoint /bin/sh demo11-dockerfile-entrypoint:v1 -c 'echo "Instrução ENTRYPOINT sobrescrita por Kalyan Reddy Daida!"'

# Saída Esperada:
# Instrução ENTRYPOINT sobrescrita por Kalyan Reddy Daida!
```

**Observação:**

- A flag `--entrypoint` sobrescreve a instrução `ENTRYPOINT` especificada no Dockerfile.
- O container executa `/bin/sh` com a opção `-c`, executando o comando `echo`.
- O container exibe `Instrução ENTRYPOINT sobrescrita por Kalyan Reddy Daida!`.

---

## Passo 3: Parar e Remover Containers e Imagens

```bash
# Pare e remova os containers
docker rm -f my-entrypoint-demo1
docker rm -f my-entrypoint-demo2
docker rm -f my-entrypoint-demo3

# Remova as imagens Docker
docker rmi demo11-dockerfile-entrypoint:v1

# Liste as imagens Docker para confirmar a remoção
docker images
```

---

## Conclusão

Você aprendeu a:

- Criar um Dockerfile usando a instrução `ENTRYPOINT`.
- Construir uma imagem Docker e executá-la, observando a execução padrão do `ENTRYPOINT`.
- Adicionar argumentos adicionais à instrução `ENTRYPOINT` durante o comando `docker run`.
- Sobrescrever a instrução `ENTRYPOINT` usando a flag `--entrypoint`.
- Marcar e enviar a imagem Docker para o Docker Hub.

---

## Notas Adicionais

- **Instrução ENTRYPOINT:**

  - A instrução `ENTRYPOINT` permite configurar um container para ser executado como um executável.
  - É útil para configurar um container que executa um comando ou aplicação específica.

- **Adicionando Argumentos:**

  - Quando você fornece argumentos adicionais durante o comando `docker run`, eles são adicionados à instrução `ENTRYPOINT`.

- **Sobrescrevendo ENTRYPOINT:**

  - Use a flag `--entrypoint` durante o comando `docker run` para sobrescrever a instrução `ENTRYPOINT` especificada no Dockerfile.

- **Melhores Práticas:**

  - Use `ENTRYPOINT` quando quiser definir um container com um executável específico.
  - Use `CMD` para fornecer argumentos padrão ao `ENTRYPOINT`.

---

## Recursos Adicionais

- [Documentação do Docker](https://docs.docker.com/)
- [Referência do Dockerfile - Instrução ENTRYPOINT](https://docs.docker.com/engine/reference/builder/#entrypoint)
- [Melhores Práticas para Escrever Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Entendendo ENTRYPOINT e CMD no Docker](https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact)

---

**Feliz Dockerização!**