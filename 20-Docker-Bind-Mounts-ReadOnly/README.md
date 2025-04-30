---
title: "Aprenda a Montar um Diretório da Máquina Host em um Contêiner Usando Bind Mounts em Modo SOMENTE LEITURA"
description: "Entenda como montar um diretório da máquina host em um contêiner Docker usando bind mounts em modo SOMENTE LEITURA com as flags `--mount` e `-v`."
---

# Aprenda a Montar um Diretório da Máquina Host em um Contêiner Usando Bind Mounts em Modo SOMENTE LEITURA

---

## Introdução

Neste guia, você aprenderá a:

1. **Montar um diretório da máquina host** em um contêiner Docker usando bind mounts em modo SOMENTE LEITURA.
2. **Usar bind mounts com permissões de somente leitura** utilizando as flags `--mount` e `-v`.
3. **Verificar a integridade e acessibilidade** dos diretórios montados.
4. **Limpar os recursos Docker** após concluir as tarefas.

Bind mounts são úteis em cenários onde você precisa que os contêineres acessem arquivos no sistema host sem modificá-los, como ao servir conteúdo estático ou arquivos de configuração que devem permanecer inalterados.

---

## Passo 1: Preparar o Diretório Host com Conteúdo Estático

Antes de montar um diretório em um contêiner Docker, certifique-se de que o diretório host existe e contém o conteúdo estático necessário.

### Passo 1.1: Revisar a Estrutura do Diretório

```bash
# Revisar Diretório
cd myfiles
```

**Explicação:**

- **`cd myfiles`**: Navega até o diretório `myfiles`, onde o conteúdo estático está localizado. Certifique-se de que este diretório contém os arquivos e subdiretórios necessários que você pretende montar no contêiner.

---

## Passo 2: Bind Mount Usando a Flag `--mount` (SOMENTE LEITURA)

A flag `--mount` fornece uma sintaxe clara e explícita para bind mounts.

### Passo 2.1: Executar o Contêiner com Bind Mount Usando `--mount`

```bash
# Navegar para o diretório 'myfiles'
cd myfiles

# Formato de Linha Única
docker run --name bind-demo3 -p 8093:80 --mount type=bind,source="$(pwd)"/static-content,target=/usr/share/nginx/html,readonly -d nginx:alpine-slim  

# Formato Legível em Múltiplas Linhas
docker run \
  --name bind-demo3 \
  -p 8093:80 \
  --mount type=bind,source="$(pwd)"/static-content,target=/usr/share/nginx/html,readonly \
  -d \
  nginx:alpine-slim  
```

**Explicação:**

- **`--name bind-demo3`**: Nomeia o contêiner como `bind-demo3`.
- **`-p 8093:80`**: Mapeia a porta `8093` do host para a porta `80` do contêiner.
- **`--mount type=bind,source="$(pwd)"/static-content,target=/usr/share/nginx/html,readonly`**:
  - **`type=bind`**: Especifica um bind mount.
  - **`source="$(pwd)"/static-content`**: Diretório no host a ser montado.
  - **`target=/usr/share/nginx/html`**: Diretório dentro do contêiner onde o diretório host será montado.
  - **`readonly`**: Monta o diretório em modo SOMENTE LEITURA, impedindo qualquer operação de escrita dentro do contêiner.
- **`-d nginx:alpine-slim`**: Executa o contêiner em modo detached usando a imagem Nginx Alpine.

### Passo 2.2: Verificar o Bind Mount

```bash
# Listar Contêineres Docker
docker ps
docker ps --format "table {{.Image}}\t{{.Names}}\t{{.Status}}\t{{.ID}}\t{{.Ports}}"
```

**Saída de Exemplo:**

```
IMAGE               NAMES         STATUS         ID                  PORTS
nginx:alpine-slim   bind-demo3    Up 10 seconds   abcdef123456        0.0.0.0:8093->80/tcp
```

**Explicação:**

- **`docker ps`**: Lista todos os contêineres Docker em execução.
- **`docker ps --format "table ..."`**: Formata a saída em uma tabela para melhor legibilidade.

### Passo 2.3: Conectar ao Contêiner e Verificar

```bash
# Conectar ao Contêiner
docker exec -it bind-demo3 /bin/sh

# Dentro do Contêiner: Verificar Uso de Disco
df -h | grep html

# Navegar para o Diretório Montado
cd /usr/share/nginx/html
ls

# Tentar Criar um Novo Arquivo (Somente Leitura)
cp index.html reddy.html

# Sair do Shell do Contêiner
exit
```

**Observações:**

1. **Verificação do Ponto de Montagem:**
   - `/usr/share/nginx/html` está montado no diretório `static-content` no host.
   - Executar `df -h | grep html` deve mostrar os detalhes do ponto de montagem.

   **Saída de Exemplo:**

   ```
   /dev/sda1                58G      3.5G     51.8G   6% /usr/share/nginx/html
   ```

2. **Integridade dos Dados:**
   - O conteúdo do diretório `static-content` está acessível dentro do contêiner.
   - **Tentar criar um novo arquivo (`reddy.html`) falhará devido às permissões SOMENTE LEITURA.**

   **Saída de Erro:**

   ```
   cp: can't create 'reddy.html': Read-only file system
   ```

3. **Acessando a Aplicação:**
   - Abra um navegador e navegue até `http://localhost:8093` para visualizar o conteúdo estático.
   - **Tentar acessar `http://localhost:8093/reddy.html` resultará em um erro 404**, confirmando que o arquivo não foi criado.

---

## Passo 3: Bind Mount Usando a Flag `-v` (SOMENTE LEITURA)

A flag `-v` ou `--volume` fornece uma sintaxe abreviada para bind mounts.

### Passo 3.1: Executar o Contêiner com Bind Mount Usando `-v`

```bash
# Navegar para o diretório contendo conteúdo estático
cd myfiles

# Formato de Linha Única
docker run --name bind-demo4 -p 8094:80 -v "$(pwd)"/static-content:/usr/share/nginx/html:ro -d nginx:alpine-slim  

# Formato Legível em Múltiplas Linhas
docker run \
  --name bind-demo4 \
  -p 8094:80 \
  -v "$(pwd)"/static-content:/usr/share/nginx/html:ro \
  -d \
  nginx:alpine-slim  
```

**Explicação:**

- **`--name bind-demo4`**: Nomeia o contêiner como `bind-demo4`.
- **`-p 8094:80`**: Mapeia a porta `8094` do host para a porta `80` do contêiner.
- **`-v "$(pwd)"/static-content:/usr/share/nginx/html:ro`**:
  - **`$(pwd)/static-content`**: Diretório no host a ser montado.
  - **`/usr/share/nginx/html`**: Diretório dentro do contêiner onde o diretório host será montado.
  - **`:ro`**: Monta o diretório em modo SOMENTE LEITURA.
- **`-d nginx:alpine-slim`**: Executa o contêiner em modo detached usando a imagem Nginx Alpine.

---

## Passo 4: Limpeza

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

- **Montar diretórios da máquina host** em contêineres Docker usando as flags `--mount` e `-v` em modo SOMENTE LEITURA.
- **Usar bind mounts com permissões de somente leitura**, impedindo que os contêineres modifiquem arquivos do host.
- **Verificar a integridade e acessibilidade** dos diretórios montados.
- **Limpar os recursos Docker** após concluir as tarefas.

Bind mounts em modo SOMENTE LEITURA são uma funcionalidade poderosa no Docker, permitindo integração segura entre sistemas host e contêineres. Eles são particularmente úteis para servir conteúdo estático, gerenciar configurações e proteger dados contra modificações não intencionais.

---

**Dockerizando com sucesso!**