---
title: "Aprenda a Popular Dados em Volumes Docker Usando Containers Docker"
description: "Entenda como popular volumes Docker usando containers com configurações de leitura-escrita e somente leitura utilizando os flags '--mount' e '-v'."
---

# Aprenda a Popular Dados em Volumes Docker Usando Containers Docker

---

## Introdução

Neste guia, você aprenderá a:

1. Criar uma imagem Docker com Nginx servindo conteúdo estático para demonstrações de volumes Docker.
2. Popular um volume Docker usando containers com permissões de leitura-escrita e somente leitura.
   - **Opção 1:** Usando o flag `--mount`.
   - **Opção 2:** Usando o flag `-v`.
3. Gerenciar volumes Docker de forma eficaz, garantindo persistência e segurança dos dados.

Os volumes Docker são essenciais para persistir dados gerados e utilizados por containers Docker. Eles permitem que os dados sobrevivam a reinicializações de containers e podem ser compartilhados entre múltiplos containers.

---

## Passo 1: Criar uma Imagem Docker com Conteúdo Estático do Nginx

### Passo 1.1: Revisar o Dockerfile

**Dockerfile**

```dockerfile
# Use nginx:alpine-slim como imagem base do Docker
FROM nginx:alpine-slim

# Labels OCI
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: Popular Volumes Docker com Containers"
LABEL org.opencontainers.image.description="Um exemplo de Dockerfile ilustrando como popular volumes Docker usando containers e servindo conteúdo estático com NGINX."
LABEL org.opencontainers.image.version="1.0"

# Usando COPY para copiar conteúdo estático local para o diretório HTML do Nginx
COPY ./static-content/ /usr/share/nginx/html
```

**Explicação:**

- **FROM nginx:alpine-slim:** Usa a imagem leve do Nginx baseada no Alpine.
- **LABELs:** Fornecem metadados sobre a imagem.
- **COPY ./static-content/ /usr/share/nginx/html:** Copia todos os arquivos do diretório `static-content` no host para o diretório HTML padrão do Nginx dentro do container.

### Passo 1.2: Revisar o Conteúdo Estático

**Estrutura do Diretório:**

```
Dockerfiles/
├── Dockerfile
└── static-content/
    ├── app1/
    │   └── index.html
    ├── file1.html
    ├── file2.html
    ├── file3.html
    ├── file4.html
    ├── file5.html
    └── index.html
```

### Passo 1.3: Construir uma Imagem Docker

```bash
# Mudar para o diretório
cd Dockerfiles

# Construir a imagem Docker
docker build -t <NOME_DA_IMAGEM>:<TAG> .
docker build -t mynginx-static:v1 .

# Listar imagens Docker
docker images

# Executar o container Docker e verificar
docker run --name=volumes-demo-base-container -p 8090:80 -d mynginx-static:v1

# Listar containers Docker
docker ps
docker ps --format "table {{.Image}}\t{{.Names}}\t{{.Status}}\t{{.ID}}\t{{.Ports}}"

# Acessar a aplicação
http://localhost:8090
Observação:
1. Todo o conteúdo estático está presente e acessível.
```

---

## Passo 2: Popular um Volume Usando um Container

Popular um volume Docker envolve montá-lo em um diretório do container. Quando um volume é montado em um diretório que já contém dados, o Docker copia os dados existentes para o volume. Isso garante que o volume comece com os dados iniciais do container.

### Opção 1: Usando o Flag `--mount`

O flag `--mount` fornece uma sintaxe mais detalhada e explícita para montar volumes.

#### Passo 2.1: Usando o Flag `--mount` com Acesso de Leitura-Escrita

**Comando:**

```bash
# Formato em Linha Única
docker run --name volume-demo1 -p 8091:80 --mount type=volume,source=myvol103,target=/usr/share/nginx/html -d mynginx-static:v1

# Formato Legível
docker run \
    --name volume-demo1 \
    -p 8091:80 \
    --mount type=volume,source=myvol103,target=/usr/share/nginx/html \
    -d \
    mynginx-static:v1
```

**Explicação:**

- `--name volume-demo1`: Nomeia o container como `volume-demo1`.
- `-p 8091:80`: Mapeia a porta `8091` do host para a porta `80` do container.
- `--mount type=volume,source=myvol103,target=/usr/share/nginx/html`: Monta o volume nomeado `myvol103` em `/usr/share/nginx/html` dentro do container.
- `-d mynginx-static:v1`: Executa o container em modo destacado usando a imagem `mynginx-static:v1`.

#### Passo 2.2: Verificar a Montagem do Volume

```bash
# Listar containers Docker
docker ps
docker ps --format "table {{.Image}}\t{{.Names}}\t{{.Status}}\t{{.ID}}\t{{.Ports}}"

# Conectar ao container
docker exec -it volume-demo1 /bin/sh

# Dentro do container: Verificar uso de disco
df -h

# Navegar até o diretório montado
cd /usr/share/nginx/html
ls

# Sair do shell do container
exit
```

**Observações:**

1. Um novo volume Docker `myvol103` é criado e montado em `/usr/share/nginx/html`.
2. O conteúdo estático da imagem Docker é copiado com sucesso para o volume.
3. Não há perda de dados; o volume contém os dados iniciais da imagem.
4. Isso demonstra a vantagem de usar volumes para persistência de dados.

#### Passo 2.3: Inspecionar o Container Docker

```bash
# Inspecionar detalhes do container
docker inspect volume-demo1

# Extrair informações de Mounts em formato JSON
docker inspect --format='{{json .Mounts}}' volume-demo1

# Exibir informações de Mounts de forma legível usando jq
docker inspect --format='{{json .Mounts}}' volume-demo1 | jq
```

**Explicação:**

- Esses comandos fornecem informações detalhadas sobre as montagens do container, mostrando que `myvol103` está corretamente montado em `/usr/share/nginx/html`.

#### Passo 2.4: Acessar a Aplicação

```bash
# Acessar via navegador
http://localhost:8091

# Acessar via curl
curl http://localhost:8091
```

**Observação:**

- Todo o conteúdo estático está acessível, confirmando que o volume foi populado corretamente.

---

## Conclusão

Você aprendeu a:

- Criar uma imagem Docker com Nginx servindo conteúdo estático.
- Popular volumes Docker usando containers com permissões de leitura-escrita e somente leitura.
  - Usar o flag `--mount` para montar volumes de forma explícita.
  - Usar o flag `-v` para montar volumes de forma abreviada.
- Verificar a integridade e as permissões dos volumes montados.
- Limpar containers, imagens e volumes Docker.

Os volumes Docker são uma funcionalidade poderosa para gerenciar dados persistentes em containers, permitindo que os dados persistam entre ciclos de vida de containers e facilitando o compartilhamento de dados entre múltiplos containers.

---

**Feliz Dockerização!**