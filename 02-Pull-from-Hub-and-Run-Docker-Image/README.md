---
title: "Como Fazer Pull e Executar Imagens Docker do Docker Hub"
description: "Aprenda como fazer pull de imagens Docker do Docker Hub e executá-las. Este guia cobre o download de imagens, execução de containers, inicialização e parada de containers, e remoção de imagens."
---

# Como Fazer Pull e Executar Imagens Docker do Docker Hub

---

## Introdução

Neste guia, você irá:

1. **Fazer pull de imagens Docker** do Docker Hub.
2. **Executar containers Docker** usando as imagens baixadas.
3. **Iniciar e parar containers Docker**.
4. **Remover imagens Docker**.
5. **Nota Importante:** Não é necessário fazer login no Docker Hub para baixar imagens públicas. Neste caso, a imagem Docker `stacksimplify/mynginx` é pública e não requer autenticação.

---

## Passo 1: Fazer Pull de Imagem Docker do Docker Hub

```bash
# Listar imagens Docker (deve estar vazio se nenhuma imagem foi baixada ainda)
docker images

# Fazer pull da imagem Docker do Docker Hub
docker pull stacksimplify/mynginx:v1

# Alternativamente, fazer pull do GitHub Packages (sem limites de download)
docker pull ghcr.io/stacksimplify/mynginx:v1

# Listar imagens Docker para confirmar que a imagem foi baixada
docker images
```

**Notas Importantes:**

1. **Limites de Pull de Imagens Docker:** O Docker Hub impõe limites de pull para usuários anônimos e gratuitos.
2. **Registro Alternativo:** Para evitar atingir os limites do Docker Hub, você pode baixar a mesma imagem Docker do **GitHub Packages**.
3. **Consistência:** Ambas as imagens são iguais; escolha entre Docker Hub ou GitHub Packages com base nas suas necessidades.

---

## Passo 2: Executar a Imagem Docker Baixada

- **Copie o nome da imagem Docker** do Docker Hub ou GitHub Packages.
- **HOST_PORT:** O número da porta no seu host onde você deseja receber tráfego (ex.: `8080`).
- **CONTAINER_PORT:** O número da porta dentro do container que está ouvindo conexões (ex.: `80`).

```bash
# Executar Container Docker
docker run --name <CONTAINER-NAME> -p <HOST_PORT>:<CONTAINER_PORT> -d <IMAGE_NAME>:<TAG>

# Exemplo usando imagem do Docker Hub:
docker run --name myapp1 -p 8080:80 -d stacksimplify/mynginx:v1

# Ou usando imagem do GitHub Packages:
docker run --name myapp1 -p 8080:80 -d ghcr.io/stacksimplify/mynginx:v1
```

**Acesse a Aplicação:**

- Abra o navegador e navegue para [http://localhost:8080/](http://localhost:8080/).

---

## Passo 3: Listar Containers Docker em Execução

```bash
# Listar apenas containers em execução
docker ps

# Listar todos os containers (incluindo os parados)
docker ps -a

# Listar apenas os IDs dos containers
docker ps -q
```

---

## Passo 4: Conectar ao Terminal do Container Docker

Você pode se conectar ao terminal de um container em execução para inspecioná-lo ou depurá-lo:

```bash
# Conectar ao terminal do container
docker exec -it <CONTAINER-NAME> /bin/sh

# Exemplo:
docker exec -it myapp1 /bin/sh

# Dentro do container, você pode executar comandos:
ls
hostname
exit  # Para sair do terminal do container
```

**Executar Comandos Diretamente:**

```bash
# Listar o conteúdo do diretório dentro do container
docker exec -it myapp1 ls

# Obter o hostname do container
docker exec -it myapp1 hostname

# Imprimir variáveis de ambiente
docker exec -it myapp1 printenv

# Verificar o uso de espaço em disco
docker exec -it myapp1 df -h
```

---

## Passo 5: Parar e Iniciar Containers Docker

```bash
# Parar um container em execução
docker stop <CONTAINER-NAME>

# Exemplo:
docker stop myapp1

# Verificar se o container foi parado
docker ps

# Testar se a aplicação está fora do ar
curl http://localhost:8080

# Iniciar o container parado
docker start <CONTAINER-NAME>

# Exemplo:
docker start myapp1

# Verificar se o container está em execução
docker ps

# Testar se a aplicação voltou ao ar
curl http://localhost:8080
```

---

## Passo 6: Remover Containers Docker

```bash
# Parar o container se ele ainda estiver em execução
docker stop <CONTAINER-NAME>
docker stop myapp1

# Remover o container
docker rm <CONTAINER-NAME>
docker rm myapp1

# Ou parar e remover o container em um único comando
docker rm -f <CONTAINER-NAME>
docker rm -f myapp1
```

---

## Passo 7: Remover Imagens Docker

```bash
# Listar imagens Docker
docker images

# Remover imagem Docker usando o ID da imagem
docker rmi <IMAGE-ID>

# Exemplo:
docker rmi abc12345def6

# Remover imagem Docker usando o Nome e Tag da imagem
docker rmi <IMAGE-NAME>:<IMAGE-TAG>

# Exemplo:
docker rmi stacksimplify/mynginx:v1
```

---

## Conclusão

Você aprendeu como fazer pull de imagens Docker do Docker Hub ou GitHub Packages, executar containers a partir dessas imagens, interagir com containers em execução e gerenciar containers e imagens na sua máquina local.

**Parabéns!**

---

## Notas Adicionais

- **Substitua os Marcadores:** Lembre-se de substituir `<CONTAINER-NAME>`, `<HOST_PORT>`, `<CONTAINER_PORT>`, `<IMAGE_NAME>` e `<TAG>` pelos seus valores reais.
- **Docker Hub vs. GitHub Packages:** Se você encontrar limites de pull no Docker Hub, considere usar o GitHub Packages (`ghcr.io`) como alternativa.
- **Nomes de Containers:** Dar nomes significativos aos seus containers ajuda a gerenciá-los facilmente.
- **Limpeza:** Remova regularmente containers e imagens não utilizados para liberar espaço em disco.

---

## Recursos Adicionais

- [Documentação do Docker](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Registro de Contêiner do GitHub](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Referência de Comandos CLI do Docker](https://docs.docker.com/engine/reference/commandline/docker/)

---


**Feliz Dockerização!**