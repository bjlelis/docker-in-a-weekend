---
title: "Aprenda as Instruções EXPOSE e RUN no Dockerfile na Prática"
description: "Crie um Dockerfile com as instruções EXPOSE e RUN para entender seu uso na construção de imagens Docker."
---

# Aprenda as Instruções EXPOSE e RUN no Dockerfile na Prática

---

## Introdução

Neste guia, você irá:

- Criar um Dockerfile do Nginx com as instruções `EXPOSE` e `RUN`.
- Criar três arquivos de configuração do Nginx ouvindo nas portas 8081, 8082 e 8083.
- Criar três arquivos HTML do Nginx, cada um servido em sua respectiva porta.
- Instalar o binário `curl` no container usando a instrução `RUN`.
- Construir a imagem Docker e verificar as instruções `RUN` e `EXPOSE`.

---

## Passo 1: Arquivos da Aplicação

### Arquivos de Configuração do Nginx

- **Diretório:** `DockerFiles/nginx-conf`

**`nginx-8081.conf`:**

```conf
server {
    listen 8081;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index-8081.html;
    }
}
```

**`nginx-8082.conf`:**

```conf
server {
    listen 8082;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index-8082.html;
    }
}
```

**`nginx-8083.conf`:**

```conf
server {
    listen 8083;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index-8083.html;
    }
}
```

### Arquivos HTML do Nginx

- **Diretório:** `DockerFiles/nginx-html`

**`index-8081.html`:**

```html
<!DOCTYPE html> 
<html> 
  <body style='background-color:rgb(135, 215, 159);'> 
    <h1>Bem-vindo ao StackSimplify - Instruções RUN e EXPOSE no Dockerfile</h1>
    <h2>Resposta do Nginx na porta 8081</h2> 
    <p>Aprenda tecnologia por meio de demonstrações práticas e reais.</p> 
    <p>Versão da Aplicação: V1</p>      
    <p>EXPOSE: Descreve em quais portas sua aplicação está ouvindo.</p>     
    <p>RUN: Executa comandos de build.</p>     
  </body>
</html>
```

**`index-8082.html`:**

```html
<!DOCTYPE html> 
<html> 
  <body style='background-color:rgb(210, 153, 152);'> 
    <h1>Bem-vindo ao StackSimplify - Instruções RUN e EXPOSE no Dockerfile</h1>
    <h2>Resposta do Nginx na porta 8082</h2> 
    <p>Aprenda tecnologia por meio de demonstrações práticas e reais.</p> 
    <p>Versão da Aplicação: V1</p>      
    <p>EXPOSE: Descreve em quais portas sua aplicação está ouvindo.</p>     
    <p>RUN: Executa comandos de build.</p>     
  </body>
</html>
```

**`index-8083.html`:**

```html
<!DOCTYPE html> 
<html> 
  <body style='background-color:rgb(227, 213, 180);'> 
    <h1>Bem-vindo ao StackSimplify - Instruções RUN e EXPOSE no Dockerfile</h1>
    <h2>Resposta do Nginx na porta 8083</h2> 
    <p>Aprenda tecnologia por meio de demonstrações práticas e reais.</p> 
    <p>Versão da Aplicação: V1</p>      
    <p>EXPOSE: Descreve em quais portas sua aplicação está ouvindo.</p>     
    <p>RUN: Executa comandos de build.</p>     
  </body>
</html>
```

**`index.html`:**

```html
<!DOCTYPE html> 
<html> 
  <body style='background-color:rgb(157, 182, 216);'> 
    <h1>Bem-vindo ao StackSimplify - Instruções RUN e EXPOSE no Dockerfile</h1>
    <h2>Resposta do Nginx na porta 80</h2> 
    <p>Aprenda tecnologia por meio de demonstrações práticas e reais.</p> 
    <p>Versão da Aplicação: V1</p>      
    <p>EXPOSE: Descreve em quais portas sua aplicação está ouvindo.</p>     
    <p>RUN: Executa comandos de build.</p>     
  </body>
</html>
```

---

## Passo 2: Criar Dockerfile

- **Diretório:** `DockerFiles`

Crie um `Dockerfile` com o seguinte conteúdo:

```dockerfile
# Use nginx:alpine-slim como imagem base do Docker
FROM nginx:alpine-slim

# Labels OCI
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: Usando as Instruções RUN e EXPOSE no Dockerfile"
LABEL org.opencontainers.image.description="Um exemplo de Dockerfile ilustrando o uso das instruções RUN e EXPOSE"
LABEL org.opencontainers.image.version="1.0"

# Copie todos os arquivos de configuração do Nginx do diretório nginx-conf
COPY nginx-conf/*.conf /etc/nginx/conf.d/

# Copie todos os arquivos HTML do diretório nginx-html
COPY nginx-html/*.html /usr/share/nginx/html/

# Instale o curl usando RUN
RUN apk --no-cache add curl

# Exponha as portas 8081, 8082, 8083 (a porta padrão 80 já está exposta na imagem base do Nginx)
EXPOSE 8081 8082 8083
```

---

## Passo 3: Construir a Imagem Docker e Executá-la

```bash
# Mude para o diretório DockerFiles
cd DockerFiles

# Construa a imagem Docker 
docker build -t [IMAGE-NAME]:[IMAGE-TAG] .

# Exemplo:
docker build -t demo8-dockerfile-expose-run:v1 .

# Inspecione os Labels
docker image inspect demo8-dockerfile-expose-run:v1

# Execute o container Docker e mapeie as portas
docker run --name my-expose-run-demo -p 8080:80 -p 8081:8081 -p 8082:8082 -p 8083:8083 -d demo8-dockerfile-expose-run:v1

# Acesse a aplicação no navegador
http://localhost:8080
http://localhost:8081
http://localhost:8082
http://localhost:8083

# Liste os arquivos de configuração no container Docker
docker exec -it my-expose-run-demo ls /etc/nginx/conf.d

# Liste os arquivos HTML no container Docker
docker exec -it my-expose-run-demo ls /usr/share/nginx/html

# Conecte-se ao shell do container
docker exec -it my-expose-run-demo /bin/sh

# Comandos para executar dentro do container
curl http://localhost
curl http://localhost:8081
curl http://localhost:8082
curl http://localhost:8083

# Saia do shell do container
exit
```

**Observações:**

1. Os comandos `curl` dentro do container Docker funcionam, o que significa que a instrução `RUN` para instalar o `curl` foi bem-sucedida.
2. Todas as portas de escuta do Nginx estão acessíveis dentro do container Docker.

---

## Passo 4: Parar e Remover Container e Imagens

```bash
# Pare e remova o container
docker rm -f my-expose-run-demo

# Remova as imagens Docker
docker rmi [DOCKER_USERNAME]/[IMAGE-NAME]:[IMAGE-TAG]
docker rmi [IMAGE-NAME]:[IMAGE-TAG]

# Exemplos:
docker rmi demo8-dockerfile-expose-run:v1

# Liste as imagens Docker para confirmar a remoção
docker images
```

---

## Conclusão

Você aprendeu a:

- Criar um Dockerfile do Nginx usando as instruções `EXPOSE` e `RUN`.
- Configurar o Nginx para ouvir em múltiplas portas adicionando arquivos de configuração personalizados.
- Servir diferentes páginas HTML em diferentes portas.
- Instalar pacotes adicionais (`curl`) dentro da imagem Docker usando a instrução `RUN`.
- Construir e executar a imagem Docker, verificando a funcionalidade das instruções `RUN` e `EXPOSE`.
- Marcar e enviar a imagem Docker para o Docker Hub.

---

## Notas Adicionais

- **Instrução EXPOSE:**
  - A instrução `EXPOSE` informa ao Docker que o container ouve nas portas de rede especificadas em tempo de execução.
  - Ela não publica as portas automaticamente; você ainda precisa usar a flag `-p` ou `-P` com `docker run` para mapear as portas.

- **Instrução RUN:**
  - A instrução `RUN` executa comandos em uma nova camada sobre a imagem atual e salva os resultados.
  - É usada para instalar pacotes de software ou qualquer comando que precise ser executado durante o processo de build da imagem.

- **Melhores Práticas:**
  - Use tags explícitas para suas imagens Docker para gerenciar versões de forma eficaz.
  - Limpe imagens e containers não utilizados para liberar espaço em disco.
  - Mantenha suas imagens Docker pequenas, minimizando o número de camadas e usando imagens base leves.

---

## Recursos Adicionais

- [Documentação do Docker](https://docs.docker.com/)
- [Referência do Dockerfile](https://docs.docker.com/engine/reference/builder/)
- [Melhores Práticas para Escrever Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Instrução EXPOSE](https://docs.docker.com/engine/reference/builder/#expose)
- [Instrução RUN](https://docs.docker.com/engine/reference/builder/#run)
- [Entendendo o Binding de Portas no Docker](https://docs.docker.com/config/containers/container-networking/)

---

**Feliz Dockerização!**