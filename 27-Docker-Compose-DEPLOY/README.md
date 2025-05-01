---
title: "Domine o Docker Compose: Implantação, Escalabilidade, Balanceamento de Carga e Persistência"
description: "Aprenda a implantar e escalar aplicações usando Docker Compose com balanceamento de carga e persistência de sessão."
---

# Domine o Docker Compose: Implantação, Escalabilidade, Balanceamento de Carga e Persistência

---

## Step-01: Introdução

Neste guia, exploraremos a opção `deploy` do Docker Compose para alcançar:

1. Escalar o serviço **app-ums** para 3 containers.
2. Usar **web-nginx** para balancear o tráfego entre os 3 containers do serviço **app-ums**.

---

## Step-02: Revisar `docker-compose.yaml`

```yaml
name: ums-stack
services:
  web-nginx:
    image: nginx:latest 
    container_name: ums-nginx
    ports:
      - "8080:8080"  # O NGINX escuta na porta 8080 do host
    depends_on:
      - app-ums
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf  # Configuração personalizada do NGINX

  app-ums:
    image: ghcr.io/stacksimplify/usermgmt-webapp-v6:latest
    ports:
      - "8080"  # Apenas expõe a porta do container, permitindo que o Docker escolha a porta do host
    deploy:
      replicas: 3  # Escala o serviço para 3 instâncias       
    depends_on:
      - db-mysql
    environment:
      - DB_HOSTNAME=db-mysql
      - DB_PORT=3306
      - DB_NAME=webappdb
      - DB_USERNAME=root
      - DB_PASSWORD=dbpassword11

  db-mysql:
    container_name: ums-mysqldb
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: dbpassword11
      MYSQL_DATABASE=webappdb
    ports:
      - "3306:3306"
    volumes:
      - mydb:/var/lib/mysql

volumes:
  mydb:
```

---

## Step-03: Revisar `nginx.conf`

```conf
events { }

http {
  resolver 127.0.0.11 ipv6=off;  
  
  upstream app-ums {
    server app-ums:8080;  
    # Persistência de sessão usando o endereço IP do cliente para aplicativos stateful (UMS)
    # ip_hash;  # Desative para ver como o balanceamento de carga funciona
  }

  server {
    listen 8080;

    location / {
      proxy_pass http://app-ums;
    }
  }
}
```

---

## Step-04: Como Iniciar a Pilha UMS

Inicie a pilha UMS seguindo estes passos:

```bash
# Alterar para o diretório do projeto
cd ums-stack

# Iniciar a pilha UMS em modo detached
docker compose up -d
```

A flag `-d` executa os serviços em segundo plano.

---

## Step-05: Verificar os Serviços

Para verificar os serviços MySQL e WebApp UMS:

```bash
# Listar containers Docker em execução
docker compose ps
```

Para visualizar os logs dos serviços:

```bash
docker compose logs db-mysql
docker compose logs app-ums 
docker compose logs web-nginx
```

Para verificar os logs de containers individuais:

```bash
docker logs <NOME-DO-CONTAINER>
docker logs ums-stack-app-ums-1
docker logs ums-stack-app-ums-2
docker logs ums-stack-app-ums-3
```

---

## Step-06: Verificar o Balanceamento de Carga

```bash
# Acessar a API que exibe o ID do container
http://localhost:8080/hello1

# Executar um loop para verificar o balanceamento de carga entre múltiplos containers app-ums
while true; do curl http://localhost:8080/hello1; echo ""; sleep 1; done
```

**Observação**:

1. As requisições serão distribuídas entre os containers.

---

## Step-07: Habilitar Persistência no NGINX

O WebApp UMS é stateful. Para habilitar a persistência de sessão e evitar problemas como falhas de login ao alternar entre containers, atualize o `nginx.conf`:

```conf
events { }

http {
  resolver 127.0.0.11 ipv6=off;  
  
  upstream app-ums {
    server app-ums:8080;  
    ip_hash;  # Habilitar persistência de sessão usando o endereço IP do cliente
  }

  server {
    listen 8080;

    location / {
      proxy_pass http://app-ums;
    }
  }
}
```

---

## Step-08: Reiniciar o Container NGINX

Após habilitar `ip_hash` no `nginx.conf`, reinicie o NGINX:

```bash
# Opção 1: Reiniciar o serviço NGINX
docker compose restart web-nginx

# Opção 2: Recarregar a configuração do NGINX sem parar o container
docker compose ps # Obter o nome do container
docker exec <nginx_container_name> nginx -s reload
docker exec ums-nginx nginx -s reload
```

---

## Step-09: Acessar o WebApp UMS

1. Abra seu navegador e navegue até `http://localhost:8080`.
2. Faça login com:
   - **Usuário**: `admin101`
   - **Senha**: `password101`
3. Você pode:
   - Visualizar a lista de usuários.
   - Criar novos usuários.
   - Testar a funcionalidade de login com os novos usuários.

---

## Step-10: Conectar ao Container MySQL

Para inspecionar ou interagir com o banco de dados MySQL, conecte-se ao container MySQL:

```bash
docker exec -it ums-mysqldb mysql -u root -pdbpassword11
```

Dentro do shell do MySQL, execute consultas SQL:

```bash
mysql> show schemas;
mysql> use webappdb;
mysql> show tables;
mysql> select * from user;
```

---

## Step-11: Verificar Comunicação entre Containers Usando Nomes de Serviço e DNS

```bash
# Listar containers Docker em execução
docker compose ps

# Conectar ao container ums-stack-app-ums-1
docker exec -it ums-stack-app-ums-1 /bin/bash

# Testar DNS - web-nginx
nslookup <NOME-DO-SERVIÇO>
nslookup web-nginx
dig web-nginx

# Testar DNS - app-ums
nslookup <NOME-DO-SERVIÇO>
nslookup app-ums
dig app-ums

# Testar DNS - db-mysql
nslookup <NOME-DO-SERVIÇO>
nslookup db-mysql
dig db-mysql
```

---

## Step-12: Parar e Limpar

Para parar e remover os containers em execução:

```bash
docker compose down
```

Para remover o volume MySQL também:

```bash
docker compose down -v
docker volume ls  # Verificar se o volume foi removido
```

---

## Conclusão

Neste guia, você aprendeu como escalar e implantar uma pilha multi-container usando Docker Compose, incluindo balanceamento de carga com NGINX e escalabilidade do WebApp UMS. Habilitamos persistência para gerenciamento de sessões, garantindo que o WebApp UMS opere de forma eficaz em um ambiente stateful.

A opção `deploy` do Docker Compose e as configurações personalizadas do NGINX oferecem poderosas capacidades de escalabilidade e balanceamento de carga para microsserviços ou aplicações multi-container.

---

## Notas Adicionais

- **Escalabilidade com Docker Compose**: A opção `deploy` ajuda a escalar serviços especificando o número de réplicas. Isso funciona em conjunto com balanceadores de carga como o NGINX para distribuir o tráfego.
- **Persistência de Sessão**: Aplicações stateful como o WebApp UMS requerem persistência de sessão. Usar `ip_hash` no NGINX garante que as requisições dos clientes sejam roteadas consistentemente para o mesmo container durante uma sessão.
- **Configuração Personalizada do NGINX**: Aproveitar o resolvedor DNS interno do Docker e as configurações personalizadas do NGINX permite controle refinado sobre o balanceamento de carga e o gerenciamento de sessões.

---

## Recursos Adicionais

- [Documentação do Docker Compose](https://docs.docker.com/compose/)
- [Documentação do NGINX](https://nginx.org/en/docs/)
- [Imagem MySQL no Docker Hub](https://hub.docker.com/_/mysql)
- [Rede Docker](https://docs.docker.com/network/)
- [Escalabilidade com Docker Compose](https://docs.docker.com/compose/production/)

---

**Feliz Dockerização!**


## Opção Deploy no Docker Compose

A opção `deploy` no Docker Compose é usada para definir configurações relacionadas à implantação de serviços. Ela é tipicamente usada no modo **Docker Swarm**, que habilita recursos de orquestração para aplicações containerizadas. Embora a opção `deploy` seja ignorada em ambientes não-swarm (como configurações locais usando Docker Compose em modo standalone), ela é crucial ao escalar e gerenciar serviços em um cluster swarm de nível de produção.

### Principais Recursos da Opção `deploy`:
- **replicas**: Define o número de instâncias (réplicas) de containers a serem executadas para um serviço.

### Notas Importantes:
- A opção `deploy` é ignorada ao usar o Docker Compose em modo standalone (não-swarm).
- Para aproveitar essas configurações, o modo Docker Swarm deve ser habilitado usando `docker swarm init`.
- Para configurações simples de desenvolvimento local, `deploy` pode ser omitido, e a escalabilidade do serviço pode ser feita manualmente com comandos como `docker-compose up --scale`.

### Quando Usar:
- Ao implantar em um ambiente de produção usando Docker Swarm, use a opção `deploy` para escalabilidade, gerenciamento de recursos e atualizações de serviços.

Em resumo, a opção `deploy` é essencial para orquestrar e gerenciar serviços em escala, especialmente em ambientes Docker Swarm.