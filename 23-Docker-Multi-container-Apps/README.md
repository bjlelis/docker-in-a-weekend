# Como Implantar Aplicações Multi-Container no Docker: MySQL e WebApp de Gerenciamento de Usuários

---

## Etapa 1: Introdução

Neste guia, vamos implantar uma aplicação multi-container usando Docker. A configuração inclui:

1. Criação de uma **rede Docker**.
2. Inicialização de um **container MySQL**.
3. Implantação de um **container WebApp de Gerenciamento de Usuários** que se conecta ao MySQL.
4. Verificação das funcionalidades da WebApp, como login de usuário, listagem e criação de novos usuários.
5. Limpeza dos recursos Docker.

---

## Etapa 2: Container do Banco de Dados MySQL

Vamos começar configurando o container do MySQL para gerenciar o banco de dados da aplicação.

### Configuração do Container MySQL

```bash
# Listar redes Docker existentes
docker network ls

# Criar uma nova rede Docker para a aplicação multi-container
docker network create ums-app

# Verificar a criação da rede
docker network ls

# Listar containers existentes
docker ps
docker ps -a

# Criar e executar o container MySQL
docker run -d     --network ums-app --network-alias mysql     --name ums-mysqldb     -v ums-mysql-data:/var/lib/mysql     -e MYSQL_ROOT_PASSWORD=dbpassword11     -e MYSQL_DATABASE=webappdb     -p 3306:3306     mysql:8.0
```

**Explicação:**

- `--network ums-app --network-alias mysql`: conecta o container MySQL à rede com o alias `mysql`.
- `-v ums-mysql-data:/var/lib/mysql`: monta um volume Docker para persistência de dados.
- Variáveis de ambiente:
  - `MYSQL_ROOT_PASSWORD`: senha do usuário root do MySQL.
  - `MYSQL_DATABASE`: cria previamente o banco de dados `webappdb`.

### Verificar Container MySQL

```bash
# Verificar se o container está em execução
docker ps

# Verificar se o volume de dados foi criado
docker volume ls

# Conectar ao container MySQL
docker exec -it ums-mysqldb mysql -u root -pdbpassword11

# Comandos MySQL para verificar o banco de dados
mysql> show schemas;
mysql> use webappdb;
mysql> show tables;
mysql> exit;
```

**Resultado Esperado:**

- O schema `webappdb` deve estar presente.

### Obter o Endereço IP do Container MySQL

```bash
# Buscar o IP do container MySQL
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ums-mysqldb
```

---

## Etapa 3: Testar o Sinalizador `--network-alias`

Vamos testar a resolução de DNS na rede Docker usando o alias `mysql`.

```bash
# Executar um container de teste para verificar a resolução DNS
docker run --name test-mysql-dns -it --network ums-app nicolaka/netshoot

# Dentro do container, executar:
dig mysql
```

**Observação:**

- O alias `mysql` deve resolver para o IP do container MySQL, confirmando a comunicação via DNS.

---

## Etapa 4: Container da WebApp de Gerenciamento de Usuários

Agora vamos configurar o container da WebApp.

### Baixar e Executar a WebApp
- [Imagem Docker: ghcr.io/stacksimplify/usermgmt-webapp-v6:latest](https://github.com/users/stacksimplify/packages/container/package/usermgmt-webapp-v6)

```bash
# Baixar a imagem da WebApp
docker pull ghcr.io/stacksimplify/usermgmt-webapp-v6:latest

# Executar o container da WebApp
docker run -d     --network ums-app     --name ums-app     -e DB_HOSTNAME=mysql     -e DB_PORT=3306     -e DB_NAME=webappdb     -e DB_USERNAME=root     -e DB_PASSWORD=dbpassword11     -p 8080:8080     ghcr.io/stacksimplify/usermgmt-webapp-v6:latest
```

**Explicação:**

- As variáveis de ambiente conectam a WebApp ao banco de dados MySQL:
  - `DB_HOSTNAME`: nome do host definido como `mysql`.
  - `DB_PORT`: porta 3306.
  - `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD`: credenciais do banco.

### Verificar a WebApp

```bash
# Listar containers em execução
docker ps 

# Verificar os logs da WebApp
docker logs -f ums-app
```

---

## Etapa 5: Verificar e Acessar a Aplicação

### Verificar o Banco de Dados

```bash
# Conectar ao MySQL
docker exec -it ums-mysqldb mysql -u root -pdbpassword11

# Comandos MySQL para verificar dados da WebApp
mysql> show schemas;
mysql> use webappdb;
mysql> show tables;
mysql> select * from user;
```

**Observação:**

- Deve existir um usuário admin padrão na tabela `user`.

### Acessar a WebApp

1. Acesse [http://localhost:8080](http://localhost:8080) no navegador.
2. Use as credenciais padrão:
   - **Usuário**: `admin101`
   - **Senha**: `password101`

### Criar um Novo Usuário

1. Preencha os seguintes dados:
   - **Usuário**: `admin102`
   - **Senha**: `password102`
   - **Nome**: `fname102`
   - **Sobrenome**: `lname102`
   - **Email**: `email102@kalyan.com`
   - **SSN**: `ssn102`

2. Faça login com o novo usuário.

---

## Etapa 6: Limpeza

```bash
# Remover todos os containers em execução
docker rm -f $(docker ps -aq)

# Remover todas as imagens Docker
docker rmi $(docker images -q)

# Remover volumes Docker (opcional)
docker volume rm ums-mysql-data 
```

---

## Conclusão

Neste guia, você implantou uma aplicação multi-container com Docker, conectando um **container MySQL** com uma **WebApp de Gerenciamento de Usuários**. A aplicação demonstrou integração funcional com o banco de dados.

O uso de redes Docker personalizadas facilita arquiteturas em microsserviços, tornando o Docker uma ferramenta essencial na implantação de aplicações modernas.

---

## Notas Adicionais

- **Rede entre Containers**: O uso de `--network` permite comunicação via DNS entre containers.
- **Persistência de Dados**: Volumes Docker garantem persistência mesmo após remoção de containers.
- **Limpeza de Containers**: Boa prática para liberar recursos e manter o ambiente limpo.

---

## Recursos Adicionais

- [Redes Docker](https://docs.docker.com/network/)
- [Volumes Docker](https://docs.docker.com/storage/volumes/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Imagem Docker do MySQL](https://hub.docker.com/_/mysql)
- [Boas Práticas com Docker](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

**Feliz Dockerizando!**