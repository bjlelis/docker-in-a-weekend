---
title: "Dominando o Docker Build Cloud: Acelere Seus Builds Docker com Builders na Nuvem e Locais"
description: "Aprenda a usar o Docker Build Cloud para builds Docker, compare o desempenho entre builders locais e na nuvem, gerencie caches de build e configure builders padrão."
---

# Dominando o Docker Build Cloud: Acelere Seus Builds Docker com Builders na Nuvem e Locais

---

## Introdução

Neste guia, você irá:

1. Criar um **Builder na Nuvem** no Docker Build Cloud.
2. Criar um **Builder Local** no Docker Desktop.
3. Construir imagens Docker usando ambos os builders e comparar as diferenças de desempenho.
4. Aprender a limpar caches de build usando o comando `docker buildx prune`.
5. Aprender a configurar o builder padrão para builds Docker usando o comando `docker buildx use BUILDER-NAME --global`.

### Nota Importante sobre o Docker Build Cloud
- O Docker Build Cloud estará disponível apenas nos novos planos Docker Pro, Team e Business.
- O Docker Build Cloud **não está disponível para uso pessoal**.

---

## Passo 1: Criar um Builder na Nuvem

- Acesse o [Docker Build Cloud](https://app.docker.com/build).
- Clique em **Create Cloud Builder**.
- **Nome do Builder na Nuvem:** `mycloud-builder1`.
- Clique em **Create**.

---

## Passo 2: Adicionar o Endpoint do Builder na Nuvem

### Usando o Docker CLI

1. **Login no Docker**

   ```bash
   docker login
   ```

2. **Adicionar o endpoint do builder na nuvem**

   Substitua `<SEU-NOME-DE-USUÁRIO-DOCKER>` pelo seu nome de usuário no Docker Hub.

   ```bash
   docker buildx create --driver cloud <SEU-NOME-DE-USUÁRIO-DOCKER>/<NOME_DO_BUILDER>
   ```

   **Exemplo com 'stacksimplify':**

   ```bash
   docker buildx create --driver cloud stacksimplify/mycloud-builder1
   ```

### Usando o Docker Desktop

1. Faça login na sua conta Docker usando o botão **Sign in** no Docker Desktop.
2. Abra as **Configurações** do Docker Desktop e navegue até a aba **Builders**.
3. Em **Available builders**, selecione **Connect to builder** e siga as instruções.

---

## Passo 3: Criar um Builder Local

1. **Criar um novo builder Buildx e configurá-lo como o builder atual**

   ```bash
   docker buildx create --name mylocal-builder1 --use
   ```

2. **Inspecionar e inicializar o builder Buildx**

   ```bash
   docker buildx inspect --bootstrap
   ```

3. **Listar instâncias de builders**

   ```bash
   docker buildx ls
   ```

---

## Passo 4: Executar o Build Usando o Builder Local

**Nota:**

- Estamos usando `--push` para enviar a imagem Docker diretamente para o Docker Hub.
- **Não** estamos usando `--load` neste contexto, pois não estamos carregando a imagem no Docker Desktop local.

```bash
# Alterar para o diretório do projeto
cd multiplatform-build-cloud-demo

# Listar imagens Docker (opcional)
docker images

# Executar o build Docker com o builder local
docker buildx build --builder mylocal-builder1 --platform linux/amd64,linux/arm64 -t <SEU-NOME-DE-USUÁRIO-DOCKER>/local-builder-demo1 --push .

# Exemplo com 'stacksimplify':
docker buildx build --builder mylocal-builder1 --platform linux/amd64,linux/arm64 -t stacksimplify/local-builder-demo1 --push .
```

**Observações:**

1. O processo de build pode levar aproximadamente **162 segundos** para ser concluído.
2. Após o build, liste as imagens Docker:

   ```bash
   docker images
   ```

3. **Nota:** A imagem Docker **não** estará presente no Docker Desktop local, pois foi enviada diretamente para o Docker Hub.

**Verificar Imagens Docker no Docker Hub:**

- Faça login na sua conta Docker Hub.
- Navegue até a seção **Repositories**.
- Você verá a imagem recém-enviada `local-builder-demo1`.

---

## Passo 5: Executar o Build Usando o Builder na Nuvem

**Nota:**

- Estamos usando `--push` para enviar a imagem Docker diretamente para o Docker Hub.
- **Não** estamos usando `--load` neste contexto, pois não estamos carregando a imagem no Docker Desktop local.

```bash
# Alterar para o diretório do projeto (se ainda não estiver lá)
cd multiplatform-build-cloud-demo

# Listar imagens Docker (opcional)
docker images

# Executar o build Docker com o builder na nuvem
docker buildx build --builder cloud-stacksimplify-mycloud-builder1 --platform linux/amd64,linux/arm64 -t <SEU-NOME-DE-USUÁRIO-DOCKER>/cloud-builder-demo101 --push .

# Exemplo com 'stacksimplify':
docker buildx build --builder cloud-stacksimplify-mycloud-builder1 --platform linux/amd64,linux/arm64 -t stacksimplify/cloud-builder-demo101 --push .
```

**Observações:**

1. O processo de build pode levar aproximadamente **18 segundos** para ser concluído.
2. Após o build, liste as imagens Docker:

   ```bash
   docker images
   ```

3. **Nota:** A imagem Docker **não** estará presente no Docker Desktop local, pois foi enviada diretamente para o Docker Hub.

**Verificar Imagens Docker no Docker Hub:**

- Faça login na sua conta Docker Hub.
- Navegue até a seção **Repositories**.
- Você verá a imagem recém-enviada `cloud-builder-demo101`.

---

## Passo 6: Configurar o Builder na Nuvem como Padrão

1. **Configurar o builder na nuvem como o builder padrão globalmente**

   ```bash
   docker buildx use cloud-stacksimplify-mycloud-builder1 --global
   ```

2. **Verificar o builder padrão**

   - Abra o Docker Desktop.
   - Navegue até **Configurações** → **Builders**.
   - **Observação:** Você verá **"cloud-stacksimplify-mycloud-builder1"** configurado como o builder padrão.

3. **Criar builds sem especificar `--builder`**

   ```bash
   docker buildx build --platform linux/amd64,linux/arm64 -t stacksimplify/cloud-builder-demo102 --push .
   ```

**Observações:**

1. O processo de build pode levar aproximadamente **12 segundos** para ser concluído.
2. **Nota:** Mesmo sem especificar `--builder`, o build usará o builder na nuvem, pois ele está configurado como padrão.

---

## Passo 7: Limpeza

1. **Listar builders do Docker Buildx**

   ```bash
   docker buildx ls
   ```

2. **Parar o builder local**

   ```bash
   docker buildx stop mylocal-builder1
   ```

3. **Remover o builder local**

   ```bash
   docker buildx rm mylocal-builder1
   ```

4. **Verificar a lista de builders**

   ```bash
   docker buildx ls
   ```

5. **Remover imagens Docker (opcional)**

   ```bash
   docker rmi $(docker images -q)
   ```

   > **Aviso:** Este comando removerá **TODAS** as imagens Docker do seu Docker Desktop local.

---

## Passo 8: Remover Caches de Build

1. **Remover cache de build para builders específicos**

   ```bash
   docker buildx prune --builder <NOME_DO_BUILDER> -f
   ```

   **Exemplos:**

   ```bash
   docker buildx prune --builder mylocal-builder1 -f
   docker buildx prune --builder cloud-stacksimplify-mycloud-builder1 -f
   ```

---

## Conclusão

Você aprendeu a usar o Docker Build Cloud, comparou diferenças de desempenho entre builders locais e na nuvem, gerenciou caches de build e configurou builders padrão. Sinta-se à vontade para experimentar mais e integrar essas práticas ao seu fluxo de trabalho Docker.

**Feliz Dockerização!**

---

## Recursos Adicionais

- [Documentação do Docker Buildx](https://docs.docker.com/buildx/working-with-buildx/)
- [Guia Oficial do Docker Build Cloud](https://docs.docker.com/docker-cloud/builds/)

---

## Notas Adicionais

- Certifique-se de substituir `<SEU-NOME-DE-USUÁRIO-DOCKER>` pelo seu nome de usuário real no Docker Hub ao longo do guia.
- Tenha cuidado ao executar `docker rmi $(docker images -q)`, pois ele removerá **TODAS** as imagens Docker do seu ambiente local.
- Os tempos de desempenho mencionados nas observações são aproximados e podem variar com base na velocidade da sua rede e nos recursos do sistema.
