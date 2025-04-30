---
title: "Aprenda a Montar um Diretório da Máquina Host em um Contêiner Usando Bind Mounts"
description: "Entenda como montar um diretório da máquina host em um contêiner Docker usando bind mounts com as flags `--mount` e `-v`."
---

# Aprenda a Montar um Diretório da Máquina Host em um Contêiner Usando Bind Mounts

---

## Introdução

Neste guia, você aprenderá a:

1. **Montar um diretório da máquina host** em um contêiner Docker usando bind mounts.
2. **Usar bind mounts com permissões de leitura e escrita** utilizando as flags `--mount` e `-v`.
3. **Verificar a integridade e acessibilidade** dos diretórios montados.
4. **Limpar os recursos Docker** após concluir as tarefas.

Bind mounts são úteis em cenários onde você precisa que os contêineres acessem ou modifiquem arquivos no sistema host, como durante o desenvolvimento ou ao compartilhar arquivos de configuração.

---

## Passo 1: Preparar o Diretório Host com Conteúdo Estático

Antes de montar um diretório em um contêiner Docker, certifique-se de que o diretório host existe e contém o conteúdo estático necessário.

### Passo 1.1: Revisar a Estrutura do Diretório

```bash
# Revisar Diretório
cd myfiles
```

---

## Passo 2: Bind Mount Usando a Flag `--mount` (Leitura e Escrita)

A flag `--mount` fornece uma sintaxe clara e explícita para bind mounts.

### Passo 2.1: Executar o Contêiner com Bind Mount Usando `--mount`

```bash
# Navegar para o diretório 'myfiles'
cd myfiles

# Formato de Linha Única
docker run --name bind-demo1 -p 8091:80 --mount type=bind,source="$(pwd)"/static-content,target=/usr/share/nginx/html -d nginx:alpine-slim  

# Formato Legível em Múltiplas Linhas
docker run \
  --name bind-demo1 \
  -p 8091:80 \
  --mount type=bind,source="$(pwd)"/static-content,target=/usr/share/nginx/html \
  -d \
  nginx:alpine-slim  
```

**Explicação:**

- **`--name bind-demo1`**: Nomeia o contêiner como `bind-demo1`.
- **`-p 8091:80`**: Mapeia a porta `8091` do host para a porta `80` do contêiner.
- **`--mount type=bind,source="$(pwd)"/static-content,target=/usr/share/nginx/html`**:
  - **`type=bind`**: Especifica um bind mount.
  - **`source="$(pwd)"/static-content`**: Diretório no host a ser montado.
  - **`target=/usr/share/nginx/html`**: Diretório dentro do contêiner onde o diretório host será montado.
- **`-d nginx:alpine-slim`**: Executa o contêiner em modo detached usando a imagem Nginx Alpine.

### Passo 2.2: Verificar o Bind Mount

```bash
# Listar Contêineres Docker
docker ps
docker ps --format "table {{.Image}}\t{{.Names}}\t{{.Status}}\t{{.ID}}\t{{.Ports}}"

# Conectar ao Contêiner
docker exec -it bind-demo1 /bin/sh

# Dentro do Contêiner: Verificar Uso de Disco
df -h | grep html

# Navegar para o Diretório Montado
cd /usr/share/nginx/html
ls

# Tentar Criar um Novo Arquivo (Leitura e Escrita)
cp index.html kalyan.html

# Sair do Shell do Contêiner
exit
```

**Observações:**

1. **Verificação do Ponto de Montagem:**
   - `/usr/share/nginx/html` está montado no diretório `static-content` no host.
   - Executar `df -h | grep html` deve mostrar os detalhes do ponto de montagem.
   
2. **Integridade dos Dados:**
   - O conteúdo do diretório `static-content` está acessível dentro do contêiner.
   - Criar um novo arquivo (`kalyan.html`) demonstra acesso de leitura e escrita.

3. **Acessando a Aplicação:**
   - Abra um navegador e navegue até `http://localhost:8091` para visualizar o conteúdo estático.
   - Acesse `http://localhost:8091/kalyan.html` para verificar o arquivo recém-criado.

### Passo 2.3: Inspecionar o Contêiner Docker

```bash
# Inspecionar Contêiner Docker
docker inspect bind-demo1

# Extrair Informações de Montagem em Formato JSON
docker inspect --format='{{json .Mounts}}' bind-demo1

# Formatar Informações de Montagem Usando jq
docker inspect --format='{{json .Mounts}}' bind-demo1 | jq  
```

**Explicação:**

- **`Type`**: Indica um bind mount.
- **`Source`**: Diretório no host.
- **`Destination`**: Diretório dentro do contêiner onde o bind mount é aplicado.
- **`RW`**: `true` indica acesso de leitura e escrita.

---

## Passo 3: Bind Mount Usando a Flag `-v` (Leitura e Escrita)

A flag `-v` ou `--volume` fornece uma sintaxe abreviada para bind mounts.

### Passo 3.1: Executar o Contêiner com Bind Mount Usando `-v`

```bash
# Navegar para o diretório contendo conteúdo estático
cd myfiles

# Formato de Linha Única
docker run --name bind-demo2 -p 8092:80 -v "$(pwd)"/static-content:/usr/share/nginx/html -d nginx:alpine-slim  

# Formato Legível em Múltiplas Linhas
docker run \
  --name bind-demo2 \
  -p 8092:80 \
  -v "$(pwd)"/static-content:/usr/share/nginx/html \
  -d \
  nginx:alpine-slim  
```

**Explicação:**

- **`--name bind-demo2`**: Nomeia o contêiner como `bind-demo2`.
- **`-p 8092:80`**: Mapeia a porta `8092` do host para a porta `80` do contêiner.
- **`-v "$(pwd)"/static-content:/usr/share/nginx/html`**:
  - **`$(pwd)/static-content`**: Diretório no host a ser montado.
  - **`/usr/share/nginx/html`**: Diretório dentro do contêiner onde o diretório host será montado.
- **`-d nginx:alpine-slim`**: Executa o contêiner em modo detached usando a imagem Nginx Alpine.

---

## Passo 4: Verificar Arquivos no Diretório Local

Após realizar operações dentro dos contêineres, é crucial verificar se as alterações são refletidas na máquina host.

```bash
# Navegar para o diretório static-content no host
cd myfiles/static-content

# Listar Arquivos
ls
```

**Observação:**

- Você deve encontrar os arquivos `kalyan.html` e `kalyan2.html` presentes:
  - **`kalyan.html`**: Criado pelo `bind-demo1`.
  - **`kalyan2.html`**: Criado pelo `bind-demo2`.

---

## Passo 5: Limpeza

Após concluir as demonstrações, é importante limpar os recursos Docker para liberar recursos do sistema e manter um ambiente organizado.

```bash
# Excluir Contêineres Docker
docker rm -f $(docker ps -aq)

# Excluir Imagens Docker
docker rmi $(docker images -q)
```

---

## Conclusão

Você aprendeu a:

- **Montar diretórios da máquina host** em contêineres Docker usando as flags `--mount` e `-v`.
- **Usar bind mounts com permissões de leitura e escrita**, permitindo que contêineres acessem e modifiquem arquivos do host.
- **Verificar a integridade e acessibilidade** dos diretórios montados.
- **Limpar os recursos Docker** após concluir as tarefas.

Bind mounts são uma funcionalidade poderosa no Docker, permitindo integração perfeita entre sistemas host e contêineres. Eles são particularmente úteis para ambientes de desenvolvimento, gerenciamento de configurações e cenários que exigem persistência e compartilhamento de dados.

---

**Dockerizando com sucesso!**