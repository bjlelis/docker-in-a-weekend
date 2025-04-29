---
title: "Aprenda a Criar e Usar Volumes no Docker"
description: "Entenda como criar e usar volumes no Docker, incluindo volumes nomeados e anônimos, utilizando tanto a CLI quanto o Docker Desktop."
---

# Aprenda a Criar e Usar Volumes no Docker

---

## Introdução

Neste guia, você aprenderá a:

- Criar volumes no Docker, tanto nomeados quanto anônimos, usando a CLI e o Docker Desktop.
- Excluir volumes usando o comando `docker volume prune`.
- Excluir volumes específicos usando o comando `docker volume rm`.

Os volumes no Docker são uma forma de persistir dados gerados e utilizados por containers Docker. Eles são o mecanismo preferido para persistir dados gerados e utilizados por containers Docker.

---

## Passo 1: Criar Volumes no Docker Usando a CLI

### Criar um Volume Nomeado

Para criar um volume nomeado no Docker usando a CLI:

```bash
# Crie um volume nomeado no Docker
docker volume create my-volume1

# Liste os volumes do Docker
docker volume ls

# Inspecione o volume do Docker
docker volume inspect my-volume1
```

**Explicação:**

- `docker volume create my-volume1` cria um novo volume nomeado chamado `my-volume1`.
- `docker volume ls` lista todos os volumes do Docker no sistema.
- `docker volume inspect my-volume1` fornece informações detalhadas sobre o volume, incluindo seu ponto de montagem no host.

### Criar um Volume Anônimo

Para criar um volume anônimo no Docker (um volume sem nome):

```bash
# Crie um volume anônimo no Docker
docker volume create

# Liste os volumes do Docker
docker volume ls

# Exemplo de saída pode mostrar um volume com um ID longo, como:
# local     a114ae62254967bb4c9933ad6fdd82a6652dd8b0933ffdb4c818e8ed1a9c13f5

# Inspecione o volume anônimo do Docker
docker volume inspect a114ae62254967bb4c9933ad6fdd82a6652dd8b0933ffdb4c818e8ed1a9c13f5
```

**Explicação:**

- Executar `docker volume create` sem especificar um nome cria um volume anônimo com um ID único.
- Volumes anônimos são frequentemente criados implicitamente quando você usa a instrução `VOLUME` em um Dockerfile sem especificar um nome.

---

## Passo 2: Criar Volumes no Docker Usando o Docker Desktop

### Criar um Volume Nomeado

Você também pode criar volumes no Docker usando o Docker Desktop:

1. Abra o Docker Desktop.
2. Navegue até a aba **Volumes**.
3. Clique em **Create**.
4. No campo **Volume Name**, insira `my-volume2`.
5. Clique em **Create**.

### Criar um Volume Anônimo

Para criar um volume anônimo (sem nome) usando o Docker Desktop:

1. Abra o Docker Desktop.
2. Navegue até a aba **Volumes**.
3. Clique em **Create**.
4. Deixe o campo **Volume Name** vazio.
5. Clique em **Create**.

---

## Passo 3: Remover Volumes Não Utilizados com `docker volume prune`

O comando `docker volume prune` é usado para remover todos os volumes locais não utilizados. Isso é útil para liberar espaço removendo volumes que não estão mais em uso.

```bash
# Remova volumes não utilizados do Docker (removerá volumes anônimos não utilizados por nenhum container)
docker volume prune

# Para confirmar a ação, digite 'y' quando solicitado.

# Remova todos os volumes não utilizados do Docker (incluindo volumes nomeados não utilizados por nenhum container)
docker volume prune -a

# Liste os volumes do Docker para verificar
docker volume ls
```

**Importante:**

- Tenha cuidado ao usar `docker volume prune -a`, pois ele removerá todos os volumes não utilizados, incluindo volumes nomeados que não estão atualmente em uso por nenhum container.
- Sempre certifique-se de que você não precisa dos dados nos volumes antes de realizar a limpeza.

---

## Passo 4: Remover Volumes do Docker com `docker volume rm`

O comando `docker volume rm` permite remover um ou mais volumes específicos.

```bash
# Crie um volume nomeado no Docker
docker volume create my-volume6

# Crie um volume anônimo no Docker
docker volume create

# Liste os volumes do Docker
docker volume ls

# Exemplo de saída:
# DRIVER    VOLUME NAME
# local     my-volume6
# local     a69ef20af8869c0631b7ecc33400a56e2b56fa0cbdf9f14deed938f4c7520051

# Remova um volume nomeado do Docker
docker volume rm my-volume6

# Remova um volume anônimo especificando seu ID
docker volume rm a69ef20af8869c0631b7ecc33400a56e2b56fa0cbdf9f14deed938f4c7520051

# Liste os volumes do Docker para confirmar a remoção
docker volume ls
```

**Nota:**

- Você não pode remover um volume que está atualmente em uso por um container.
- Se você tentar remover tal volume, o Docker retornará um erro.

---

## Conclusão

Você aprendeu a:

- Criar volumes no Docker, tanto nomeados quanto anônimos, usando a CLI e o Docker Desktop.
- Listar e inspecionar volumes do Docker.
- Remover volumes não utilizados usando `docker volume prune`.
- Remover volumes específicos usando `docker volume rm`.

---

## Notas Adicionais

- **Volumes no Docker:**

  - Os volumes do Docker são armazenados em uma parte do sistema de arquivos do host gerenciada pelo Docker (`/var/lib/docker/volumes/` no Linux).
  - Volumes são o mecanismo preferido para persistir dados gerados e utilizados por containers Docker.

- **Melhores Práticas:**

  - Use volumes nomeados quando precisar persistir dados e compartilhá-los entre múltiplos containers.
  - Tenha cuidado ao limpar volumes para evitar perda acidental de dados.
  - Limpe regularmente volumes não utilizados para liberar espaço em disco.

- **Diferença Entre Volumes Nomeados e Anônimos:**

  - **Volumes Nomeados:** Têm um nome específico que você atribui e podem ser facilmente referenciados em múltiplos containers.
  - **Volumes Anônimos:** Não têm um nome específico e são identificados por um ID longo. Eles são frequentemente usados quando você precisa de um volume, mas não precisa compartilhá-lo entre containers.

---

## Recursos Adicionais

- [Documentação do Docker - Volumes](https://docs.docker.com/storage/volumes/)
- [Referência de Comandos CLI do Docker](https://docs.docker.com/engine/reference/commandline/docker/)
- [Gerenciando Dados em Containers](https://docs.docker.com/storage/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

---

**Feliz Dockerização!**