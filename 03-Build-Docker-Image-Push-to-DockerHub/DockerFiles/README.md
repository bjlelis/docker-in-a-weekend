---
title: "Como Criar e Enviar Imagens Docker para o Docker Hub: Um Guia Passo a Passo"
description: "Aprenda como criar uma imagem Docker, marcá-la e enviá-la para o Docker Hub. Este tutorial cobre a criação de uma conta no Docker Hub, criação de Dockerfile, construção de imagens, marcação e envio para o Docker Hub."
---

# Como Criar e Enviar Imagens Docker para o Docker Hub: Um Guia Passo a Passo

---

## Introdução

Neste guia, você irá:

1. Criar uma conta no Docker Hub.
2. Fazer login com seu Docker ID no Docker Desktop.
3. Fazer login no Docker Hub usando o Docker CLI.
4. Executar uma imagem base do Nginx no Docker.
5. Criar um `Dockerfile` e um `index.html` personalizados.
6. Construir uma imagem Docker a partir do `Dockerfile`.
7. Marcar e enviar a imagem Docker para o Docker Hub.
8. Pesquisar e explorar imagens Docker no Docker Hub.

> **Nota Importante:** Nos comandos abaixo, onde você vir `stacksimplify`, substitua pelo seu nome de usuário do Docker Hub.

---

## Passo 1: Criar Conta no Docker Hub

- Visite [Docker Hub](https://hub.docker.com/) e crie uma nova conta.

> **Nota:** Não é necessário fazer login no Docker Hub para baixar imagens públicas. Por exemplo, a imagem Docker `stacksimplify/mynginx` é uma imagem pública.

---

## Passo 2: Fazer Login no Docker Desktop

- Abra o **Docker Desktop**.
- Clique em **Sign In** e faça login com seu Docker ID.

---

## Passo 3: Verificar Versão do Docker e Fazer Login via Linha de Comando

```
# Verificar a versão do Docker
docker version

# Fazer login no Docker Hub
docker login

# Para sair do Docker Hub
docker logout
```

---

## Passo 4: Executar o Container Base do Nginx

- Consulte a [Imagem Docker do NGINX no Docker Hub](https://hub.docker.com/_/nginx).

```
# Executar a imagem padrão do Nginx no Docker
docker run --name <CONTAINER-NAME> -p <HOST_PORT>:<CONTAINER_PORT> -d <IMAGE_NAME>:<TAG>

# Exemplo:
docker run --name myapp1 -p 8090:80 -d nginx

# Listar containers Docker em execução
docker ps

# Acessar a aplicação no navegador
http://localhost:8090

# Parar e remover o container Docker
docker stop myapp1
docker rm myapp1

# Ou remover o container forçadamente
docker rm -f myapp1
```

---

## Passo 5: Criar Dockerfile e `index.html` Personalizado

- **Diretório:** `Dockerfiles`

**Crie um `Dockerfile`:**

```dockerfile
FROM nginx
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

## Passo 6: Construir a Imagem Docker e Executá-la

```
# Mude para o diretório que contém seu Dockerfile
cd Dockerfiles

# Construa a imagem Docker
docker build -t <IMAGE_NAME>:<TAG> .

# Exemplo:
docker build -t mynginx-custom:v1 .

# Liste as imagens Docker
docker images

# Execute o container Docker e verifique
docker run --name <CONTAINER-NAME> -p <HOST_PORT>:<CONTAINER_PORT> -d <IMAGE_NAME>:<TAG>

# Exemplo:
docker run --name mynginx1 -p 8090:80 -d mynginx-custom:v1

# Acesse a aplicação no navegador
http://localhost:8090
```

---

## Passo 7: Marcar e Enviar a Imagem Docker para o Docker Hub

```
# Liste as imagens Docker
docker images

# Marque a imagem Docker
docker tag mynginx-custom:v1 YOUR_DOCKER_USERNAME/mynginx-custom:v1

# Exemplo com 'stacksimplify':
docker tag mynginx-custom:v1 stacksimplify/mynginx-custom:v1

# Envie a imagem Docker para o Docker Hub
docker push YOUR_DOCKER_USERNAME/mynginx-custom:v1

# Exemplo com 'stacksimplify':
docker push stacksimplify/mynginx-custom:v1

# NOTA IMPORTANTE:
# Substitua YOUR_DOCKER_USERNAME pelo seu nome de usuário real do Docker Hub.
```

---

## Passo 8: Verificar a Imagem Docker no Docker Hub

- Faça login no Docker Hub e verifique a imagem que você enviou.
- Navegue até seus repositórios: [Repositórios do Docker Hub](https://hub.docker.com/repositories).

---

## Passo 9: Explorar a Interface Web do Docker Hub

- Visite [Docker Hub](https://hub.docker.com/).
- Pesquise por imagens Docker.
- Use filtros para refinar os resultados da pesquisa.

---

## Passo 10: Usar o Comando de Pesquisa do Docker

```
# Pesquisar por imagens 'nginx'
docker search nginx

# Limitar os resultados da pesquisa a 5
docker search nginx --limit 5

# Filtrar resultados da pesquisa por estrelas (ex.: imagens com pelo menos 50 estrelas)
docker search --filter=stars=50 nginx

# Filtrar apenas imagens oficiais
docker search --filter=is-official=true nginx
```

---

## Conclusão

Você criou com sucesso uma imagem Docker, marcou-a e enviou-a para o Docker Hub. Também aprendeu como pesquisar imagens usando a interface web do Docker Hub e o CLI do Docker.

**Parabéns!**

---

## Notas Adicionais

- **Substitua os Marcadores:** Lembre-se de substituir `<YOUR-DOCKER-USERNAME>`, `<CONTAINER-NAME>`, `<HOST_PORT>`, `<CONTAINER_PORT>`, `<IMAGE_NAME>` e `<TAG>` pelos seus valores reais.
- **Nome de Usuário do Docker Hub:** Certifique-se de estar logado com sua conta do Docker Hub ao enviar imagens.
- **Repositórios Públicos vs. Privados:** O Docker Hub permite repositórios públicos ilimitados para contas gratuitas. Repositórios privados podem exigir uma assinatura paga.
- **Limpeza:** Para remover imagens e containers não utilizados, você pode usar `docker system prune`, mas tenha cuidado, pois isso removerá todos os dados não utilizados.

---

## Recursos Adicionais

- [Documentação do Docker](https://docs.docker.com/)
- [Introdução ao Docker Hub](https://docs.docker.com/docker-hub/)
- [Melhores Práticas para Escrever Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---