---
title: "Aprenda a Criar Builds Docker de Estágio Único e Multi-Estágio para Aplicativos Node.js"
description: "Aprenda a criar builds Docker de estágio único e multi-estágio para aplicativos Node.js"
---

# Aprenda a Criar Builds Docker de Estágio Único e Multi-Estágio para Aplicativos Node.js

---

## Passo 1: Introdução

1. **Crie um aplicativo simples em Node.js.**
2. **Crie um build de estágio único e verifique o tamanho da imagem Docker.**
3. **Crie um build multi-estágio e verifique o tamanho da imagem Docker.**

---

## Passo 2: Estágio Único: Criar um Aplicativo Simples em Node.js

- **Pastas:** `01-nodejsapp-singlestage` e `02-nodejsapp-multistage`

### Passo 2.1: `package.json`

- **Localização:** Ambas as pastas (`01-nodejsapp-singlestage` e `02-nodejsapp-multistage`)

```json
{
  "name": "multistage-node-app",
  "version": "1.0.0",
  "description": "Um aplicativo Node.js de exemplo com build Docker multi-estágio",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "author": "KALYAN REDDY DAIDA",
  "license": "ISC",
  "dependencies": {
    "express": "^4.18.2"
  }
}
```

### Passo 2.2: `index.js`

- **Localização:** Ambas as pastas (`01-nodejsapp-singlestage` e `02-nodejsapp-multistage`)

```javascript
const express = require('express');
const app = express();
const port = process.env.PORT || 8080;

app.get('/', (req, res) => {
  res.send('Hello from Node.js app!');
});

app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);
});
```

---

## Passo 3: Aplicativo Node.js - Estágio Único: Criar Dockerfile, Build, Executar, Verificar Logs e Limpar

### Passo 3.1: Criar Dockerfile de Estágio Único

- **Pasta:** `01-nodejsapp-singlestage`

```dockerfile
# Dockerfile de estágio único para aplicativo Node.js
FROM node:bookworm

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências
COPY package*.json ./
RUN npm install --production

# Copiar o código-fonte do aplicativo
COPY *.js .

# Expor a porta do aplicativo
EXPOSE 8080

# Iniciar o aplicativo
CMD ["npm", "start"]
```

### Passo 3.2: Construir Imagem Docker, Executar, Verificar Logs e Limpar

- **Comandos:**

```bash
# Alterar para o diretório
cd 01-nodejsapp-singlestage

# Construir a imagem Docker
docker build -t nodejs-hello-singlestage .

# Listar imagens Docker
docker images 

# Executar o container Docker
docker run --name nodejsapp-singlestage -d -p 8091:8080 nodejs-hello-singlestage

# Verificar logs
docker logs -f nodejsapp-singlestage

# Acessar o aplicativo
curl localhost:8091

# Parar e remover o container
docker stop nodejsapp-singlestage
docker rm nodejsapp-singlestage
```

---

## Passo 4: Aplicativo Node.js - Multi-Estágio: Criar Dockerfile, Build, Executar, Verificar Logs e Limpar

### Passo 4.1: Criar Dockerfile Multi-Estágio

- **Pasta:** `02-nodejsapp-multistage`

```dockerfile
##### Estágio 1: Estágio de Build #####
FROM node:bookworm AS builder

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências
COPY package*.json ./
RUN npm install --production

# Copiar o código-fonte do aplicativo
COPY *.js .

##### Estágio 2: Estágio Final ##### 
FROM node:bookworm-slim AS final  

# Definir diretório de trabalho
WORKDIR /app

# Copiar os arquivos necessários do estágio de build
COPY --from=builder /app ./

# Expor a porta do aplicativo
EXPOSE 8080

# Iniciar o aplicativo
CMD ["npm", "start"]
```

### Passo 4.2: Construir Imagem Docker, Executar, Verificar Logs e Limpar

- **Comandos:**

```bash
# Alterar para o diretório
cd 02-nodejsapp-multistage

# Construir a imagem Docker
docker build -t nodejs-hello-multistage .

# Listar imagens Docker 
docker images 

# Executar o container Docker
docker run --name nodejsapp-multistage -d -p 8092:8080 nodejs-hello-multistage

# Verificar logs
docker logs -f nodejsapp-multistage

# Acessar o aplicativo
curl localhost:8092

# Parar e remover o container
docker stop nodejsapp-multistage
docker rm nodejsapp-multistage
```

---

## Passo 5: Revisar os Tamanhos das Imagens Docker

```bash
# Listar imagens Docker
docker images
```

**Observação:**

1. **Diferença de Tamanho:**
   - `nodejs-hello-singlestage`: Aproximadamente **1.62GB**
   - `nodejs-hello-multistage`: Aproximadamente **328MB**

2. **Conclusão:**
   - Usar Dockerfiles multi-estágio reduz significativamente o tamanho da imagem ao eliminar camadas e arquivos desnecessários na imagem final.

---

## Passo 6: Limpar

```bash
# Remover imagens Docker
docker rmi nodejs-hello-singlestage
docker rmi nodejs-hello-multistage
```

---

**Feliz Dockerização!**