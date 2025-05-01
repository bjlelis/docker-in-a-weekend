---
title: "Aprenda Sobre Docker BuildKit (Builder) e Buildx (CLI do Lado do Cliente)"
description: "Domine o Docker BuildKit e Buildx para melhorar seus processos de build no Docker com desempenho aprimorado e novas funcionalidades."
---

# Aprenda Sobre Docker BuildKit (Builder) e Buildx (CLI do Lado do Cliente)

---

## Step-01: Introdução

O Docker Build implementa uma arquitetura cliente-servidor, onde:

- **Cliente:** Buildx é o cliente e a interface do usuário para executar e gerenciar builds.
- **Servidor:** BuildKit é o servidor, ou builder, que lida com a execução do build.

### BuildKit - Em Detalhes

1. **BuildKit** é um backend aprimorado que substitui o builder legado.
2. **BuildKit** é o builder padrão para usuários do Docker Desktop e Docker Engine a partir da versão 23.0.
3. **BuildKit** fornece novas funcionalidades e melhora o desempenho dos seus builds.
4. Para um entendimento completo, consulte a [Documentação do BuildKit](https://docs.docker.com/build/buildkit/).

---

## Step-02: Comandos Docker Buildx - Versão e Lista

```bash
# Mostrar informações da versão do buildx
docker buildx version

# Listar instâncias de builders
docker buildx ls

# Observação:
# 1. Lista os builders pré-configurados como parte da instalação do Docker Desktop.
```

---

## Step-03: Verificar Instâncias de Builders Usando o Docker Desktop

1. Abra o **Docker Desktop**.
2. Navegue até **Configurações** > **Builders**.
3. Revise as instâncias de builders padrão que foram criadas.

---

## Step-04: Comandos Docker Buildx - `du` e `prune`

```bash
# Verificar uso de disco
docker buildx du

# Remover cache de build
docker buildx prune

# Verificar uso de disco novamente
docker buildx du
```

---

## Step-05: Comandos Docker Buildx - Inspecionar

```bash
# Inspecionar a instância de builder atual
docker buildx inspect

# Inspecionar uma instância de builder específica
docker buildx inspect --builder desktop-linux
docker buildx inspect --builder default
```

---

## Step-06: Docker Buildx - Alternar Builders

```bash
# Listar instâncias de builders
docker buildx ls

# Observação:
# 1. Observe a estrela (*) ao lado do nome do builder indicando o builder configurado atualmente.

# Alternar para o builder padrão e verificar
docker context use default
docker buildx ls

# Observação:
# 1. Vá para Docker Desktop > Configurações > Builders para verificar o builder ativo.

# Alternar de volta para o builder desktop-linux
docker context use desktop-linux
docker buildx ls

# Observação:
# 1. Vá para Docker Desktop > Configurações > Builders para verificar o builder ativo.
```

---

## Step-07: Criar e Inicializar um Novo Builder

```bash
# Criar um novo builder Buildx
docker buildx create --name mybuilder1 --use 
[ou]
docker buildx create --name mybuilder1 --use --bootstrap

# Explicação:
# - `create`: Cria uma nova instância de builder.
# - `--name mybuilder1`: Nome do novo builder.
# - `--use`: Alterna automaticamente para o builder recém-criado.
# - `--bootstrap`: Inicializa o builder após a criação.

# Inspecionar e inicializar o builder Buildx
docker buildx inspect --bootstrap

# Explicação:
# - `inspect`: Inspeciona a instância de builder atual.
# - `--bootstrap`: Garante que o builder foi inicializado antes de inspecionar.

# Listar instâncias de builders
docker buildx ls

# Listar containers Docker
docker ps

# Observação:
# Verifique se o container Buildx está em execução.

# Verificar o builder usando o Docker Desktop:
# 1. Abra o Docker Desktop.
# 2. Navegue até Configurações > Builders.
# 3. Confirme que 'mybuilder1' está listado e ativo.
```

---

## Referências Adicionais

- [Referência do Comando Docker Buildx Create](https://docs.docker.com/engine/reference/commandline/buildx_create/)
- [Documentação do BuildKit](https://docs.docker.com/build/buildkit/)
- [Documentação do Docker Buildx](https://docs.docker.com/buildx/working-with-buildx/)

---