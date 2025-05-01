---
title: "Implantar Banco de Dados MySQL Usando Docker Compose com Volumes Nomeados"
description: "Guia passo a passo para implantar um banco de dados MySQL usando Docker Compose com volumes nomeados para armazenamento persistente e gerenciamento de containers."
---

# Implantar Banco de Dados MySQL Usando Docker Compose com Volumes Nomeados

---

## Step-01: Introdução

Este tutorial demonstra como implantar um banco de dados **MySQL** usando Docker Compose com volumes nomeados para armazenamento persistente. A configuração consiste em:

- **Banco de Dados MySQL**: Gerencia o armazenamento de dados de usuários.
- **Volume Nomeado do Docker**: Garante o armazenamento persistente dos dados do banco de dados MySQL, mesmo após desligamentos ou exclusões de containers.

---

## Step-02: Pré-requisitos

Certifique-se de ter os seguintes itens instalados na sua máquina antes de executar este tutorial:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Step-03: Estrutura do Projeto

```bash
mysqldb-named-volume/
├── docker-compose.yaml   # Arquivo de configuração do Docker Compose
```

---

## Step-04: Serviços

1. **Serviço MySQL**:
   - Usa a imagem oficial `mysql:8.0` do Docker Hub.
   - Configura credenciais e esquema do banco de dados via variáveis de ambiente.
   - O container MySQL é exposto na porta `3306` da máquina host.
   - Os dados são persistidos em um volume nomeado do Docker (`mydb`), garantindo que o banco permaneça intacto mesmo após o container ser parado ou removido.

### docker-compose.yaml

```yaml
name: ums-stack
services:
  mysql:
    container_name: ums-mysqldb
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: dbpassword11
      MYSQL_DATABASE: webappdb
    ports:
      - "3306:3306"
    volumes:
      - mydb:/var/lib/mysql

volumes:
  mydb:
    name: ums-mysqldb-data-v1  # Nome explícito do volume
    driver: local  # Opcional, pois local é o driver padrão
    labels:
      project: "ums-stack"           # Rótulo para indicar o nome do projeto
      component: "mysql-database"    # Rótulo para especificar que este volume é para o banco de dados MySQL
      purpose: "persistent-storage"  # Rótulo para indicar o propósito deste volume
```

### Configuração Principal

- **`MYSQL_ROOT_PASSWORD`**: A senha root para o servidor MySQL.
- **`MYSQL_DATABASE`**: O nome do banco de dados a ser criado na inicialização (`webappdb`).
- **Portas**: O serviço MySQL é acessível em `localhost:3306`.
- **Volumes**: Um volume Docker chamado `mydb` garante o armazenamento persistente de dados em `/var/lib/mysql` dentro do container MySQL.

### Explicação dos Volumes:

- **`mydb`**: Define um volume nomeado para armazenamento persistente, garantindo que os dados não sejam perdidos quando os containers forem parados ou removidos.
  
  - **`name: ums-mysqldb-data-v1`**: Nomeia explicitamente o volume como `ums-mysqldb-data-v1`, facilitando o gerenciamento e a identificação nos comandos do Docker.
  
  - **`driver: local`**: Especifica o driver do volume como `local`, que é o driver padrão do Docker. Pode ser omitido, mas é mencionado aqui para maior clareza.
  
  - **`labels`**: Adiciona metadados ao volume usando rótulos:
    - **`project: "ums-stack"`**: Associa o volume ao nome do projeto (`ums-stack`).
    - **`component: "mysql-database"`**: Especifica que este volume está associado ao componente do banco de dados MySQL.
    - **`purpose: "persistent-storage"`**: Indica claramente o propósito do volume, que é fornecer armazenamento persistente para o banco de dados, garantindo que os dados permaneçam intactos em reinicializações ou remoções de containers.

Com esta configuração, os dados no container MySQL são armazenados com segurança fora do ciclo de vida do container. Mesmo que o container seja removido ou reiniciado, os dados armazenados em `/var/lib/mysql` (dentro do container) persistirão porque estão mapeados para o volume nomeado `ums-mysqldb-data-v1`.

---

## Step-05: Como Iniciar os Containers

Execute o seguinte comando para iniciar o container MySQL e seu volume associado:

```bash
# Iniciar o container MySQL em modo detached
docker compose up -d
```

- A flag `-d` executa os serviços em modo detached (em segundo plano).

---

## Step-06: Verificar os Serviços

Para verificar se o container MySQL está em execução:

```bash
# Listar containers em execução
docker compose ps
```

Para inspecionar os logs do container MySQL:

```bash
# Ver logs do container MySQL
docker compose logs mysql
```

---

## Step-07: Conectar ao Container MySQL

Conecte-se ao container MySQL e interaja com o banco de dados:

```bash
# Conectar ao container MySQL
docker exec -it ums-mysqldb mysql -u root -pdbpassword11
```

- Uma vez no shell do MySQL, você pode executar consultas SQL para interagir com o banco de dados `webappdb`.

---

## Step-08: Inspecionar o Volume Docker

Inspecione o volume Docker para armazenamento persistente de dados:

```bash
# Listar volumes Docker
docker volume ls

# Inspecionar detalhes do volume
docker volume inspect ums-stack_mydb
```

**Observação:**
- Este comando fornece informações detalhadas sobre o volume Docker, como caminhos de montagem e uso.

---

## Step-09: Parar e Limpar

Para parar e remover os containers, use os seguintes comandos:

```bash
# Parar e remover os containers
docker compose down
```

Para remover o volume MySQL também (opcional):

```bash
# Parar containers e remover volumes
docker compose down -v

# Listar volumes Docker para confirmar a remoção
docker volume ls
```

**Observação:**
- Executar `docker compose down -v` também removerá o volume nomeado, excluindo os dados persistentes.

---

## Conclusão

Neste tutorial, implantamos um banco de dados MySQL usando Docker Compose com volumes nomeados para armazenamento persistente. Esta configuração garante que os dados permaneçam disponíveis mesmo após os containers serem parados ou removidos. Esta configuração básica pode ser facilmente expandida adicionando serviços adicionais, como aplicativos web, que interajam com o banco de dados MySQL.

---

## Notas Adicionais

- **Armazenamento Persistente**: Volumes Docker garantem que os dados permaneçam disponíveis mesmo após a exclusão dos containers.
- **Variáveis de Ambiente**: As variáveis `MYSQL_ROOT_PASSWORD` e `MYSQL_DATABASE` simplificam a configuração do MySQL ao pré-configurar o banco de dados na inicialização.
- **Escalabilidade**: O Docker Compose permite a fácil escalabilidade dos serviços, permitindo que componentes adicionais, como aplicativos web, sejam adicionados de forma transparente.

---

## Recursos Adicionais

- [Documentação do Docker Compose](https://docs.docker.com/compose/)
- [Imagem MySQL no Docker Hub](https://hub.docker.com/_/mysql)
- [Gerenciamento de Volumes Docker](https://docs.docker.com/storage/volumes/)
- [Rede Docker](https://docs.docker.com/network/)
- [Guia de Solução de Problemas do Docker](https://docs.docker.com/config/containers/troubleshoot/)

---

**Feliz Dockerização!**