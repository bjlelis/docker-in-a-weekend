---
title: "Implantar Banco de Dados MySQL Usando Docker Compose com Armazenamento Persistente"
description: "Guia passo a passo para implantar um banco de dados MySQL usando Docker Compose, com armazenamento persistente utilizando volumes Docker, configuração de rede e gerenciamento de containers."
---

# Implantar Banco de Dados MySQL Usando Docker Compose com Armazenamento Persistente

---

## Step-01: Introdução

Este tutorial demonstra como implantar um banco de dados **MySQL** usando Docker Compose. A configuração consiste em:

- **Banco de Dados MySQL**: Atua como o backend para armazenar dados de usuários.
- **Volume Docker**: Fornece armazenamento persistente, garantindo que os dados do banco permaneçam intactos mesmo que o container seja parado ou removido.

Em tutoriais futuros, adicionaremos o **User Management WebApp (UMS WebApp)** a esta configuração do Docker Compose para criar uma pilha completa de aplicativos.

---

## Step-02: Pré-requisitos

Antes de executar este tutorial, certifique-se de ter os seguintes itens instalados na sua máquina:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Step-03: Estrutura do Projeto

```bash
mysqldb/
├── docker-compose.yaml   # Arquivo de configuração do Docker Compose
```

---

## Step-04: Serviços

### Serviço MySQL:

- Usa a imagem oficial `mysql:8.0` do Docker Hub.
- Credenciais e esquema do banco de dados são configurados via variáveis de ambiente.
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
```

### Configuração Principal

- **`MYSQL_ROOT_PASSWORD`**: A senha root para o servidor MySQL.
- **`MYSQL_DATABASE`**: O nome do banco de dados a ser criado na inicialização (`webappdb`).
- **Portas**: O serviço MySQL é acessível em `localhost:3306`.
- **Volumes**: Um volume Docker chamado `mydb` é usado para armazenamento persistente de dados em `/var/lib/mysql` dentro do container MySQL.

---

## Step-05: Como Iniciar os Containers

Execute os seguintes comandos para iniciar o container MySQL junto com seu volume associado:

```bash
# Alterar para o diretório do projeto
cd mysqldb

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

Para inspecionar os logs dos containers em execução:

```bash
# Ver logs do container MySQL
docker compose logs mysql
```

---

## Step-07: Conectar ao Container MySQL

Você pode se conectar ao container MySQL e interagir com o banco de dados:

```bash
# Conectar ao container MySQL
docker exec -it ums-mysqldb mysql -u root -pdbpassword11
```

- Uma vez no shell do MySQL, você pode executar consultas SQL para interagir com o banco de dados `webappdb`.

---

## Step-08: Inspecionar o Volume Docker

Inspecione o volume Docker criado para armazenamento persistente de dados:

```bash
# Listar volumes Docker
docker volume ls

# Inspecionar detalhes do volume
docker volume inspect ums-stack_mydb
```

**Observação:**

- Este comando fornece informações detalhadas sobre o volume, como caminhos de montagem e uso.

---

## Step-09: Parar e Limpar

Quando terminar, pare e remova os containers com os seguintes comandos:

```bash
# Parar e remover os containers
docker compose down
```

Para remover o volume MySQL também (opcional):

```bash
# Iniciar os containers
docker compose up -d

# Listar volumes Docker
docker volume ls

# Parar containers e remover volumes
docker compose down -v

# Listar volumes Docker
docker volume ls

# Observação: O volume Docker deve ser excluído como parte do comando `docker compose down -v`.
```

---

## Conclusão

Neste tutorial, implantamos um banco de dados MySQL usando Docker Compose. O banco foi configurado com armazenamento persistente usando volumes Docker, garantindo que os dados permaneçam disponíveis mesmo quando os containers forem parados ou removidos. Os próximos passos incluem adicionar serviços adicionais, como um aplicativo web, para interagir com este banco de dados MySQL.

---

## Notas Adicionais

- **Armazenamento Persistente**: Usar volumes Docker como `mydb` garante que os dados permaneçam disponíveis mesmo após a exclusão dos containers.
- **Variáveis de Ambiente**: As variáveis `MYSQL_ROOT_PASSWORD` e `MYSQL_DATABASE` simplificam a configuração do MySQL, pré-configurando o banco de dados.
- **Rede Docker**: A rede Docker criada em tutoriais futuros permitirá que vários containers se comuniquem de forma transparente.
- **Escalabilidade**: O Docker Compose facilita a escalabilidade dos serviços, e componentes adicionais, como aplicativos web, podem ser adicionados simplesmente modificando o arquivo `docker-compose.yaml`.

---

## Recursos Adicionais

- [Documentação do Docker Compose](https://docs.docker.com/compose/)
- [Imagem MySQL no Docker Hub](https://hub.docker.com/_/mysql)
- [Rede Docker](https://docs.docker.com/network/)
- [Gerenciamento de Volumes Docker](https://docs.docker.com/storage/volumes/)
- [Solução de Problemas com Containers Docker](https://docs.docker.com/config/containers/troubleshoot/)

---

**Feliz Dockerização!**