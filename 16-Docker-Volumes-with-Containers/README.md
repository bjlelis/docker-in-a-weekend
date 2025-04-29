---
title: "Aprenda a Usar Volumes do Docker com Containers Docker"
description: "Entenda como usar volumes do Docker com containers utilizando os flags '--mount' e '-v'."
---

# Aprenda a Usar Volumes do Docker com Containers Docker

---

## Introdução

Neste guia, você aprenderá a:

- Criar volumes do Docker ao iniciar containers.
- Usar os flags `--mount` e `-v` para montar volumes em containers.

Os volumes do Docker são essenciais para persistir dados gerados e utilizados por containers Docker. Eles são o método preferido para gerenciar dados em containers Docker.

---

## Passo 1: Iniciar um Container com um Volume Usando o Flag `--mount`

O flag `--mount` é a forma mais recente e detalhada de especificar montagens de volumes no Docker. Ele fornece uma sintaxe mais clara e mais opções do que o flag `-v`.

### Formato em Linha Única

```bash
# Inicie um container com um volume nomeado usando o flag --mount
docker run --name volume-demo1 -p 8090:80 --mount type=volume,source=myvol101,target=/myapps -d nginx:alpine-slim
```

### Formato Legível

```bash
docker run \
    --name volume-demo1 \
    -p 8090:80 \
    --mount type=volume,source=myvol101,target=/myapps \
    -d \
    nginx:alpine-slim
```

**Explicação:**

- `--mount type=volume,source=myvol101,target=/myapps`:
  - `type=volume`: Especifica que estamos montando um volume do Docker.
  - `source=myvol101`: O nome do volume do Docker a ser usado. Se não existir, o Docker o criará.
  - `target=/myapps`: O diretório dentro do container onde o volume será montado.

**Verificar o Container e a Montagem do Volume**

```bash
# Liste os containers Docker
docker ps

# Formate a saída para maior clareza
docker ps --format "table {{.Image}}\t{{.Names}}\t{{.Status}}\t{{.ID}}\t{{.Ports}}"

# Conecte-se ao container
docker exec -it volume-demo1 /bin/sh

# Dentro do container, verifique os volumes montados
df -h

# Navegue até o diretório montado
cd /myapps

# Liste o conteúdo (deve estar vazio inicialmente)
ls

# Saia do shell do container
exit
```

**Inspecionar o Container Docker**

```bash
# Inspecione as montagens do container
docker inspect volume-demo1

# Extraia apenas as informações de Mounts em formato JSON
docker inspect --format='{{json .Mounts}}' volume-demo1

# Para melhor legibilidade, envie a saída para o 'jq' (processador JSON)
docker inspect --format='{{json .Mounts}}' volume-demo1 | jq
```

**Saída Esperada:**

- A seção `Mounts` deve mostrar que `myvol101` está montado em `/myapps` dentro do container.
- Dentro do container, o diretório `/myapps` corresponde ao volume do Docker `myvol101`.

---

## Passo 2: Iniciar um Container com um Volume Usando o Flag `-v`

O flag `-v` ou `--volume` é a sintaxe mais antiga para montar volumes. Ele ainda é amplamente utilizado e funciona bem para montagens de volumes simples.

### Formato em Linha Única

```bash
# Inicie um container com um volume nomeado usando o flag -v
docker run --name volume-demo2 -p 8091:80 -v myvol102:/myapps -d nginx:alpine-slim
```

### Formato Legível

```bash
docker run \
    --name volume-demo2 \
    -p 8091:80 \
    -v myvol102:/myapps \
    -d \
    nginx:alpine-slim
```

**Explicação:**

- `-v myvol102:/myapps`:
  - `myvol102`: O nome do volume do Docker a ser usado. Se não existir, o Docker o criará.
  - `/myapps`: O diretório dentro do container onde o volume será montado.

**Verificar o Container e a Montagem do Volume**

```bash
# Liste os containers Docker
docker ps

# Formate a saída para maior clareza
docker ps --format "table {{.Image}}\t{{.Names}}\t{{.Status}}\t{{.ID}}\t{{.Ports}}"

# Conecte-se ao container
docker exec -it volume-demo2 /bin/sh

# Dentro do container, verifique os volumes montados
df -h

# Navegue até o diretório montado
cd /myapps

# Liste o conteúdo (deve estar vazio inicialmente)
ls

# Saia do shell do container
exit
```

**Saída Esperada:**

- A seção `Mounts` (visualizável via `docker inspect volume-demo2`) deve mostrar que `myvol102` está montado em `/myapps` dentro do container.
- Dentro do container, o diretório `/myapps` corresponde ao volume do Docker `myvol102`.

---

## Limpeza

Após concluir os passos, é uma boa prática limpar os recursos do Docker para liberar espaço no sistema.

```bash
# Pare e remova todos os containers
docker rm -f $(docker ps -aq)

# Remova todas as imagens Docker (use com cautela)
docker rmi $(docker images -q)

# Remova os volumes, se desejado
docker volume rm myvol101 myvol102

# Verifique se os volumes foram removidos
docker volume ls
```

**Nota:**

- Tenha cuidado com o comando `docker rmi $(docker images -q)`, pois ele removerá todas as imagens Docker do seu sistema.
- Certifique-se de que você não precisa das imagens antes de executar este comando.
- O mesmo se aplica à remoção de volumes. Remova apenas volumes que você não precisa mais.

---

## Conclusão

Você aprendeu a:

- Criar volumes do Docker ao iniciar containers.
- Usar o flag `--mount` para montar volumes em containers com opções explícitas.
- Usar o flag `-v` como uma forma abreviada para montar volumes em containers.
- Verificar as montagens de volumes dentro dos containers.
- Limpar containers, imagens e volumes do Docker.

---

## Notas Adicionais

- **Diferença Entre `--mount` e `-v`:**

  - O flag `--mount` é mais detalhado, mas fornece uma sintaxe clara e suporta todas as opções de volume.
  - O flag `-v` é mais curto, mas pode ser ambíguo e não suporta todas as opções de volume.

- **Quando Usar Cada Flag:**

  - Use `--mount` quando precisar de mais controle sobre as configurações do volume e quiser uma sintaxe clara.
  - Use `-v` para montagens de volumes simples e diretas.

- **Persistência de Volumes:**

  - Os dados armazenados em volumes do Docker persistem mesmo após a remoção do container.
  - Isso é útil para manter dados entre reinicializações ou atualizações de containers.

- **Casos de Uso Comuns para Volumes:**

  - Armazenar dados de banco de dados.
  - Compartilhar arquivos de configuração entre containers.
  - Persistir dados de aplicações gerados pelo container.

---

## Recursos Adicionais

- [Documentação do Docker - Usar Volumes](https://docs.docker.com/storage/volumes/)
- [Referência do Comando Docker Run](https://docs.docker.com/engine/reference/run/)
- [Drivers de Armazenamento do Docker](https://docs.docker.com/storage/)
- [Diferenças Entre `-v` e `--mount`](https://docs.docker.com/storage/#choose-the--v-or---mount-flag)

---

**Feliz Dockerização!**