---
title: Aprenda as diferenças entre Volumes Docker e Bind Mounts quando montados em um diretório não vazio em um contêiner
description: Aprenda as diferenças entre Volumes Docker e Bind Mounts quando montados em um diretório não vazio em um contêiner
---

## Passo 01: Introdução
1. Aprenda as diferenças entre Volumes Docker e Bind Mounts quando montados em um diretório não vazio em um contêiner.
2. Crie uma imagem Docker com conteúdo estático do Nginx.
3. Monte um volume em um contêiner usando a flag `--mount` (type=volume).
4. Use Bind Mount em um contêiner com a flag `--mount` (type=bind).
5. Observe as diferenças:
    - O volume irá preservar os dados anteriores do contêiner.
    - O Bind Mount irá ocultar os dados anteriores do contêiner.

---

## Passo 02: Criar uma nova imagem Docker para esta demonstração
### Passo 02-01: Revisar o Dockerfile
```bash
# Use nginx:alpine-slim como imagem base
FROM nginx:alpine-slim

# Labels OCI
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: Docker Volumes vs Bind Mounts"
LABEL org.opencontainers.image.description="Aprenda as diferenças entre Volumes Docker e Bind Mounts quando montados em um diretório não vazio em um contêiner"
LABEL org.opencontainers.image.version="1.0"

# Usando COPY para copiar arquivos locais
COPY ./static-content/ /usr/share/nginx/html
```

### Passo 02-02: Revisar o conteúdo estático que será usado pelo Nginx
- **Pasta:** Dockerfiles/static-content
    - file1.html
    - file2.html
    - file3.html
    - file4.html
    - file5.html
    - index.html
    - app1/index.html

### Passo 02-03: Construir uma imagem Docker
```bash
# Alterar para o diretório Dockerfiles
cd Dockerfiles

# Construir a imagem Docker
docker build -t <NOME_IMAGEM>:<TAG> .
docker build -t mynginx-nonemptydir:v1 .

# Listar imagens Docker
docker images

# Executar o contêiner Docker e verificar
docker run --name=nonemtpydir-demo1 -p 8095:80 -d mynginx-nonemptydir:v1

# Listar contêineres Docker
docker ps
docker ps --format "table {{.Image}}\t{{.Names}}\t{{.Status}}\t{{.ID}}\t{{.Ports}}"

# Conectar ao contêiner e verificar
docker exec -it nonemtpydir-demo1 /bin/sh

# Executar comandos dentro do contêiner
cd /usr/share/nginx/html
ls
```

**Observação:**
1. Todos os arquivos estáticos estão presentes.

**Saída de exemplo:**
```
/usr/share/nginx/html # ls
50x.html    file1.html  file3.html  file5.html
app1        file2.html  file4.html  index.html
```

**Acessar a aplicação:**
- URL: `http://localhost:8095`

**Observação:**
1. Todo o conteúdo estático está presente e acessível.

---

## Passo 03: Volume: Montar um volume em um contêiner usando a flag `--mount`
- Se você iniciar um contêiner que cria um novo volume e o contêiner tiver arquivos ou diretórios no diretório a ser montado, como `/app/`, o Docker copia o conteúdo do diretório para o volume.
- O contêiner então monta e usa o volume, e outros contêineres que usam o volume também têm acesso ao conteúdo pré-populado.

```bash
# Verificar volumes existentes
docker volume ls

# Formato de linha única: Usando a opção --mount com o volume no contêiner como /usr/share/nginx/html
docker run --name nonemtpydir-volume-demo -p 8096:80 --mount type=volume,source=myvol103,target=/usr/share/nginx/html -d mynginx-nonemptydir:v1

# Formato legível: Usando a opção --mount com o volume no contêiner como /usr/share/nginx/html
docker run \
    --name nonemtpydir-volume-demo \
    -p 8096:80 \
    --mount type=volume,source=myvol103,target=/usr/share/nginx/html \
    -d \
    mynginx-nonemptydir:v1

# Listar contêineres Docker
docker ps
docker ps --format "table {{.Image}}\t{{.Names}}\t{{.Status}}\t{{.ID}}\t{{.Ports}}"

# Conectar ao contêiner e verificar
docker exec -it nonemtpydir-volume-demo /bin/sh

# Executar comandos dentro do contêiner
df -h
cd /usr/share/nginx/html
ls
exit
```

**Observação:**
1. Um novo volume Docker foi criado e montado no contêiner.
2. O conteúdo anterior de `/usr/share/nginx/html` foi copiado com sucesso para o volume Docker.
3. **Sem perda de dados.**
4. **Esta é a maior vantagem.**

**Inspecionar o contêiner Docker:**
```bash
docker inspect nonemtpydir-volume-demo
docker inspect --format='{{json .Mounts}}' nonemtpydir-volume-demo
docker inspect --format='{{json .Mounts}}' nonemtpydir-volume-demo | jq
```

**Acessar a aplicação:**
- URL: `http://localhost:8096`

**Observação:**
1. Todo o conteúdo estático está presente e acessível.

---

## Passo 04: Bind Mount: Usar Bind Mount com a flag `--mount` e permissão de leitura e escrita
```bash
# Alterar para o diretório myfiles
cd myfiles

# Formato de linha única: Usando a opção --mount com type=bind e destino no contêiner como /usr/share/nginx/html
docker run --name nonemtpydir-bind-demo -p 8097:80 --mount type=bind,source="$(pwd)"/static-content,target=/usr/share/nginx/html -d mynginx-nonemptydir:v1

# Formato legível: Usando a opção --mount com type=bind e destino no contêiner como /usr/share/nginx/html
docker run \
  --name nonemtpydir-bind-demo \
  -p 8097:80 \
  --mount type=bind,source="$(pwd)"/static-content,target=/usr/share/nginx/html \
  -d \
  mynginx-nonemptydir:v1

# Listar contêineres Docker
docker ps
docker ps --format "table {{.Image}}\t{{.Names}}\t{{.Status}}\t{{.ID}}\t{{.Ports}}"

# Conectar ao contêiner e verificar
docker exec -it nonemtpydir-bind-demo /bin/sh

# Executar comandos dentro do contêiner
df -h
cd /usr/share/nginx/html
ls
exit
```

**Saída de exemplo:**
```
/usr/share/nginx/html # ls
local1.html
/usr/share/nginx/html #
```

**Observação:**
1. Todo o conteúdo presente no contêiner em `/usr/share/nginx/html` foi ocultado.
2. Apenas o conteúdo do diretório local da máquina host está presente em `/usr/share/nginx/html`.
3. Isso pode ser útil para testar uma nova versão da aplicação sem criar uma nova imagem, apenas criando um novo contêiner e montando o código atualizado.
4. **Nota importante:** Tenha cuidado ao montar Bind Mounts em diretórios não vazios no contêiner, pois isso pode causar problemas na aplicação.
5. Os prós e contras dependem do caso de uso.

**Acessar a aplicação:**
- URL: `http://localhost:8097/local1.html`

**Observação:**
1. Todo o conteúdo estático da máquina host está presente e acessível.
2. O sistema de arquivos é de leitura e escrita.

**Inspecionar o contêiner Docker:**
```bash
docker inspect nonemtpydir-bind-demo
docker inspect --format='{{json .Mounts}}' nonemtpydir-bind-demo
docker inspect --format='{{json .Mounts}}' nonemtpydir-bind-demo | jq
```

---

## Passo 05: Limpeza
```bash
# Excluir contêineres Docker
docker rm -f $(docker ps -aq)

# Excluir imagens Docker
docker rmi $(docker images -q)
```