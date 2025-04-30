---
title: "Armazenamento Docker - Aprenda a Usar um tmpfs Mount em um Contêiner"
description: "Aprenda como usar um tmpfs mount em um contêiner Docker para armazenamento efêmero."
---

# Armazenamento Docker - Aprenda a Usar um tmpfs Mount em um Contêiner

---

## Introdução

Neste guia, você aprenderá a:

1. **Usar um tmpfs mount em um contêiner Docker** para armazenamento efêmero.
2. **Entender as opções adicionais** disponíveis para tmpfs mounts.
3. **Reconhecer as limitações** de usar tmpfs mounts.
4. **Limpar os recursos Docker** após concluir as tarefas.

Os **tmpfs mounts** são sistemas de armazenamento temporário que residem na memória do sistema host. Eles são úteis para cenários que exigem armazenamento rápido e efêmero, que não persiste após o contêiner ser interrompido.

---

## Passo 1: Introdução aos tmpfs Mounts

Antes de usar tmpfs mounts, é essencial entender o que eles são e quando utilizá-los.

- **tmpfs Mounts:**
  - Armazenam dados na RAM do sistema host.
  - Os dados são **efêmeros** e **não persistem** após o contêiner ser interrompido.
  - Ideais para necessidades de armazenamento temporário, como cache ou dados sensíveis que não devem ser gravados em disco.

---

## Passo 2: Usar um tmpfs Mount em um Contêiner

Esta seção demonstra como criar e usar um tmpfs mount em um contêiner Docker.

### Passo 2.1: Executar um Contêiner Docker com tmpfs Mount

```bash
# Executar um contêiner Docker com um tmpfs mount em /app
docker run --name tmpfs-demo --mount type=tmpfs,destination=/app -d nginx:alpine-slim
```

**Explicação:**

- **`--name tmpfs-demo`**: Nomeia o contêiner como `tmpfs-demo`.
- **`--mount type=tmpfs,destination=/app`**:
  - **`type=tmpfs`**: Especifica que um tmpfs mount está sendo usado.
  - **`destination=/app`**: O diretório dentro do contêiner onde o tmpfs mount será anexado.
- **`-d nginx:alpine-slim`**: Executa o contêiner em modo detached usando a imagem leve Nginx Alpine.

### Passo 2.2: Verificar o tmpfs Mount

```bash
# Listar contêineres Docker em execução
docker ps

# Inspecionar os detalhes do tmpfs mount
docker inspect tmpfs-demo --format '{{ json .Mounts }}'
```

**Explicação:**

- **`Type`**: Indica um tmpfs mount.
- **`Destination`**: O ponto de montagem dentro do contêiner (`/app`).
- **`RW`**: `true` indica acesso de leitura e escrita ao tmpfs mount.

### Passo 2.3: Testar a Persistência do tmpfs Mount

```bash
# Conectar ao contêiner
docker exec -it tmpfs-demo /bin/sh

# Dentro do contêiner: Verificar o uso de disco para confirmar o tmpfs mount
df -h | grep /app

# Navegar para o diretório do tmpfs mount
cd /app
ls

# Criar arquivos de exemplo no tmpfs mount
echo "conteúdo do arquivo1" > file1.html
echo "conteúdo do arquivo2" > file2.html
ls

# Sair do shell do contêiner
exit

# Parar o contêiner Docker
docker stop tmpfs-demo

# Reiniciar o contêiner Docker
docker start tmpfs-demo

# Reconectar ao contêiner
docker exec -it tmpfs-demo /bin/sh

# Dentro do contêiner: Verificar o conteúdo do tmpfs mount
df -h | grep /app
cd /app
ls
exit

# Observação:
# 1. O diretório /app está vazio após reiniciar o contêiner.
# 2. Os arquivos criados dentro do tmpfs mount não persistem entre reinicializações do contêiner.
```

**Explicação:**

- **Criação de Arquivos:** Demonstra que você pode gravar no tmpfs mount enquanto o contêiner está em execução.
- **Teste de Persistência:** Após parar e reiniciar o contêiner, o diretório `/app` está vazio, confirmando que os tmpfs mounts são efêmeros.

---

## Passo 3: Opções Adicionais para tmpfs

O Docker permite especificar opções adicionais para tmpfs mounts para controlar seu comportamento.

### Passo 3.1: Verificar o Tamanho do tmpfs Mount

Por padrão, os tmpfs mounts têm um tamanho máximo de 50% da RAM total do host. Você pode personalizar isso usando a opção `tmpfs-size`.

```bash
# Executar um contêiner Docker com um tmpfs mount de 100MB
docker run --name tmpfs-demo-size --mount type=tmpfs,destination=/app,tmpfs-size=100m -d nginx:alpine-slim

# Inspecionar o contêiner para verificar o tamanho do tmpfs
docker inspect tmpfs-demo-size --format '{{ json .Mounts }}' | jq
```

**Saída de Exemplo:**

```json
[
  {
    "Type": "tmpfs",
    "Source": "",
    "Destination": "/app",
    "Mode": "",
    "RW": true,
    "Propagation": "",
    "Options": {
      "size": "100m"
    }
  }
]
```

**Explicação:**

- **`tmpfs-size=100m`**: Define o tamanho máximo do tmpfs mount para 100 megabytes.

---

## Passo 4: Limitações dos tmpfs Mounts

Embora os tmpfs mounts ofereçam benefícios, eles também possuem certas limitações:

1. **Armazenamento Efêmero:**
   - Os dados armazenados em tmpfs mounts **não persistem** após o contêiner ser interrompido.
   - Não são adequados para dados que precisam ser mantidos entre reinicializações do contêiner.

2. **Sem Compartilhamento Entre Contêineres:**
   - Diferentemente dos volumes Docker, os tmpfs mounts **não podem ser compartilhados** entre múltiplos contêineres.

3. **Consumo de Memória:**
   - Os tmpfs mounts consomem **RAM**. O uso excessivo pode levar ao esgotamento da memória no host.

---

## Passo 5: Limpeza

Após concluir as demonstrações, é importante limpar os recursos Docker para liberar recursos do sistema e manter um ambiente organizado.

```bash
# Excluir todos os contêineres Docker
docker rm -f $(docker ps -aq)

# Excluir todas as imagens Docker
docker rmi $(docker images -q)

# Opcionalmente, remover volumes Docker não utilizados
docker volume prune -f
```

**Explicação:**

- **`docker rm -f $(docker ps -aq)`**: Remove forçadamente todos os contêineres Docker, em execução ou parados.
- **`docker rmi $(docker images -q)`**: Remove todas as imagens Docker do sistema. *Use com cautela.*
- **`docker volume prune -f`**: Remove todos os volumes Docker não utilizados. A flag `-f` força a operação sem solicitar confirmação.

---

## Conclusão

Você aprendeu a:

- **Usar um tmpfs mount em um contêiner Docker**, habilitando armazenamento efêmero na memória.
- **Configurar opções adicionais** para tmpfs mounts, como definir limites de tamanho.
- **Testar o comportamento de persistência** dos tmpfs mounts, confirmando sua natureza efêmera.
- **Entender as limitações** dos tmpfs mounts, incluindo a falta de persistência e capacidade de compartilhamento.
- **Limpar os recursos Docker** para manter um ambiente limpo.

Os **tmpfs mounts** são poderosos para cenários que exigem armazenamento rápido e temporário, que não persiste além do ciclo de vida do contêiner. Eles são ideais para cache, processamento temporário de dados e armazenamento de informações sensíveis que não devem ser gravadas em disco.

---

## Notas Adicionais

- **tmpfs vs. Volumes Docker:**
  - **tmpfs Mounts:**
    - Armazenam dados na RAM.
    - Efêmeros e não persistem após o contêiner ser interrompido.
    - Não podem ser compartilhados entre contêineres.
  
  - **Volumes Docker:**
    - Armazenam dados no sistema de arquivos do host.
    - Persistem dados entre reinicializações do contêiner.
    - Podem ser compartilhados entre múltiplos contêineres.

- **Gerenciamento de Memória:**
  - Monitore o uso de memória do sistema host ao usar tmpfs mounts para evitar esgotamento de recursos.
  
- **Considerações de Segurança:**
  - Como os tmpfs mounts residem na memória, eles podem ser mais seguros para dados sensíveis, pois não são gravados em disco.
  
- **Casos de Uso:**
  - Cache de dados temporários.
  - Armazenamento de informações sensíveis, como chaves de API ou tokens.
  - Armazenamento temporário para processos de build ou tarefas de processamento de dados.

---

## Recursos Adicionais

- [Documentação Docker - tmpfs Mounts](https://docs.docker.com/storage/tmpfs/)
- [Referência CLI do Docker](https://docs.docker.com/engine/reference/commandline/docker/)
- [Entendendo os Drivers de Armazenamento Docker](https://docs.docker.com/storage/storagedriver/select-storage-driver/)
- [Melhores Práticas Docker](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Segurança Docker - Usando Volumes com Segurança](https://docs.docker.com/engine/security/security/#docker-volumes)

---

**Dockerizando com sucesso!**