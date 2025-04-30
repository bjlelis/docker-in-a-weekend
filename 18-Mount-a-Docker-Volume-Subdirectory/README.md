---
title: "Aprenda a Montar um Subdiretório de Volume em um Contêiner"
description: "Entenda como montar um subdiretório de um volume Docker em um contêiner usando a flag `--mount`."
---

# Aprenda a Montar um Subdiretório de Volume em um Contêiner

---

## Introdução

Neste guia, você aprenderá a:

1. **Usar a flag `volume-subpath`** ao montar volumes em contêineres.
2. **Montar subdiretórios** de um volume Docker em diretórios específicos dentro de um contêiner.

Montar subdiretórios de volumes Docker permite um controle mais granular sobre o compartilhamento e a persistência de dados, possibilitando que os contêineres acessem apenas as partes necessárias de um volume.

---

## Passo 1: Revisar o Volume Docker

Antes de montar, é essencial entender o estado atual dos volumes Docker.

```bash
# Listar Volumes Docker
docker volume ls

# Exemplo de Saída:
DRIVER    VOLUME NAME
local     myvol103
```

### Verificar Conteúdo no Volume

1. **Usando o Docker Desktop:**
   - Abra o Docker Desktop.
   - Navegue até **Volumes**.
   - Selecione **`myvol103`**.
   - Clique em **Stored data** para visualizar o conteúdo.
   - Você deve ver o diretório `app1` populado com conteúdo estático.

**Explicação:**

- **`myvol103`**: Este é o volume Docker que usaremos para montar um subdiretório.
- **Diretório `app1`**: Contém conteúdo estático específico que pretendemos montar no contêiner.

---

## Passo 3: Montar um Subdiretório de Volume Usando a Flag `--mount`

Montar um subdiretório de um volume Docker permite acessar apenas uma parte específica do volume dentro do contêiner.

### Executar o Contêiner com o Subdiretório de Volume Montado

Montaremos o subdiretório `app1` do volume `myvol103` em `/usr/share/nginx/html/app1` dentro do contêiner.

```bash
# Formato de Linha Única
docker run --name volume-demo6 -p 8096:80 --mount type=volume,source=myvol103,target=/usr/share/nginx/html/app1,volume-subpath=app1 -d nginx:alpine-slim

# Formato Legível em Múltiplas Linhas
docker run \
    --name volume-demo6 \
    -p 8096:80 \
    --mount type=volume,source=myvol103,target=/usr/share/nginx/html/app1,volume-subpath=app1 \
    -d \
    nginx:alpine-slim
```

**Explicação:**

- **`--name volume-demo6`**: Nomeia o contêiner como `volume-demo6`.
- **`-p 8096:80`**: Mapeia a porta `8096` do host para a porta `80` do contêiner.
- **`--mount type=volume,source=myvol103,target=/usr/share/nginx/html/app1,volume-subpath=app1`**:
  - **`type=volume`**: Especifica que um volume Docker está sendo usado.
  - **`source=myvol103`**: Nome do volume Docker a ser montado.
  - **`target=/usr/share/nginx/html/app1`**: Diretório dentro do contêiner onde o volume será montado.
  - **`volume-subpath=app1`**: Especifica o subdiretório dentro do volume a ser montado. *(Nota: A partir do Docker 20.10+, `volume-subpath` é usado principalmente no Docker Compose. No `docker run`, especificar o `target` para um subdiretório alcança funcionalidade semelhante.)*

### Verificar a Montagem do Volume

```bash
# Listar Contêineres Docker
docker ps
docker ps --format "table {{.Image}}\t{{.Names}}\t{{.Status}}\t{{.ID}}\t{{.Ports}}"
```

**Exemplo de Saída:**

```
IMAGE               NAMES           STATUS         ID                  PORTS
nginx:alpine-slim   volume-demo6    Up 10 seconds   abcdef123456        0.0.0.0:8096->80/tcp
```

### Conectar ao Contêiner e Verificar

```bash
# Conectar ao Contêiner
docker exec -it volume-demo6 /bin/sh

# Dentro do Contêiner: Verificar Uso de Disco
df -h | grep app1

# Navegar até o Diretório Montado
cd /usr/share/nginx/html/app1
ls

# Sair do Shell do Contêiner
exit
```

**Saída Esperada Dentro do Contêiner:**

```
/usr/share/nginx/html # df -h | grep app1
/dev/vda1                58.4G      3.5G     51.8G   6% /usr/share/nginx/html/app1

/usr/share/nginx/html # ls
index.html
app1/
```

**Observação:**

1. **Ponto de Montagem:** `/usr/share/nginx/html/app1` está corretamente montado no subdiretório `app1` do volume `myvol103`.
2. **Integridade dos Dados:** O conteúdo estático do diretório `app1` está presente no subdiretório montado, garantindo que não haja perda de dados.
3. **Vantagens:** Montar subdiretórios permite compartilhamento seletivo de dados e melhor organização dentro dos contêineres.

### Acessar a Aplicação

```bash
# Acessar via Navegador
http://localhost:8096/app1/index.html

# Acessar via curl
curl http://localhost:8096/app1/index.html
```

**Saída Esperada:**

```html
<!DOCTYPE html> 
<html> 
  <body style='background-color:rgb(136, 209, 144);'> 
    <h1>Bem-vindo ao StackSimplify - App1 - Subdiretório de Volume "/app1"</h1> 
    <p>Aprenda tecnologia por meio de demonstrações práticas e reais.</p> 
    <p>Versão da Aplicação: V1</p>     
  </body>
</html>
```

**Observação:**

- O conteúdo estático do subdiretório `app1` está acessível e corretamente servido pelo Nginx.
- Isso confirma que a montagem do subdiretório está funcionando conforme o esperado.

### Inspecionar o Contêiner Docker

```bash
# Inspecionar Contêiner Docker
docker inspect volume-demo6

# Extrair Informações de Montagem em Formato JSON
docker inspect --format='{{json .Mounts}}' volume-demo6

# Formatar Informações de Montagem Usando jq
docker inspect --format='{{json .Mounts}}' volume-demo6 | jq
```

**Explicação:**

- Esses comandos fornecem informações detalhadas sobre as montagens do contêiner.
- Usar `jq` ajuda a formatar a saída JSON para melhor legibilidade.

**Exemplo de Saída:**

```json
[
  {
    "Type": "volume",
    "Name": "myvol103",
    "Source": "/var/lib/docker/volumes/myvol103/_data",
    "Destination": "/usr/share/nginx/html/app1",
    "Driver": "local",
    "Mode": "",
    "RW": true,
    "Propagation": ""
  }
]
```

**Observação:**

- Confirma que `myvol103` está montado em `/usr/share/nginx/html/app1` dentro do contêiner.
- **`RW: true`** indica que a montagem é de leitura e escrita.

---

## Passo 4: Limpeza

Após concluir a demonstração, é importante limpar os recursos Docker para liberar recursos do sistema e manter um ambiente organizado.

```bash
# Excluir Contêineres Docker
docker rm -f $(docker ps -aq)

# Excluir Imagens Docker
docker rmi $(docker images -q)

# Listar Volumes Docker
docker volume ls

# Observação: 
# Volumes persistem e não são excluídos mesmo após a exclusão de contêineres ou imagens

# Excluir Volume Específico
docker volume remove myvol103
```

**Explicação:**

- **`docker rm -f $(docker ps -aq)`**: Remove forçadamente todos os contêineres Docker, em execução ou parados.
- **`docker rmi $(docker images -q)`**: Remove todas as imagens Docker do sistema. *Use com cautela.*
- **`docker volume ls`**: Lista todos os volumes Docker para verificar quais ainda existem.
- **`docker volume remove myvol103`**: Exclui o volume Docker específico `myvol103`.

**Nota:**

- **Persistência de Dados:** Volumes Docker persistem dados mesmo após a remoção de contêineres ou imagens, garantindo que dados importantes não sejam perdidos acidentalmente.
- **Limpeza Seletiva:** Sempre verifique se você não precisa dos dados dentro de um volume antes de removê-lo para evitar perda acidental de dados.

---

## Conclusão

Você aprendeu a:

- **Montar um subdiretório** de um volume Docker em um contêiner usando a flag `--mount`.
- **Verificar a integridade e acessibilidade** do subdiretório montado dentro do contêiner.
- **Acessar a aplicação** para confirmar que o conteúdo estático foi servido corretamente.
- **Inspecionar o contêiner Docker** para entender a configuração de montagem.
- **Limpar os recursos Docker** removendo contêineres, imagens e volumes.

Montar subdiretórios de volumes Docker melhora o gerenciamento de dados, permitindo controle preciso sobre quais partes do volume são acessíveis dentro dos contêineres. Essa abordagem é benéfica para organizar dados, melhorar a segurança e otimizar o uso de recursos.

---

**Dockerizando com sucesso!**