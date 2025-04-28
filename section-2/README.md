**Comandos básicos para a seção 2:**
```
# Fazer o pull de uma imagem a partir do docker hub:
docker pull stacksimplify/mynginx:v1 

# Rodar um container docker:
docker run --name myapp1 -p 8080:80 -d stacksimplify/mynginx:v1

# Conectar em um container:
docker exec -it myapp1 /bin/sh
docker exec -it myapp1 hostname

# Iniciar ou parar containers:
docker stop myapp1
docker start myapp1

#Remover containers:
docker rm myapp1

# Remover forçadamente:
docker rm -f myapp1
```

**Nesta seção iremos:**
- Fazer o pull de docker images a partir do docker hub
- Rodar container usando as imagens baixadas
- Start e stop de containers
Remover idocker images

---

**Passo 1:**

```
# Listar Docker images: 
docker images

# Pull de Docker image do Docker Hub:
docker pull stacksimplify/mynginx:v1

# Listar Docker images para confirmar que a imagem foi baixada para o registry local:
docker images
```

**Passo 2: Executar a imagem baixada**

- Copiar o nome da imagem
- Definir a porta onde receberá o host tráfego: HOST_PORT
- Definir a porta onde o container receberá o tráfego: CONTAINER_PORT
- Após os passos abaixo, você estará apto a acessar a aplicação em **http://localhost:8080**

```
# Rodar o Docker Container
docker run --name <CONTAINER-NAME> -p <HOST_PORT>:<CONTAINER_PORT> -d <IMAGE_NAME>:<TAG>

# Example usando a Docker Hub image:
docker run --name myapp1 -p 8080:80 -d stacksimplify/mynginx:v1
```

**Passo 3: Listar container em execução**

```
# Listar apenas running containers
docker ps

# Listar todos os containers 
docker ps -a

# List apenas container IDs
docker ps -q
```

**Step 4: Conectar a um Container Terminal**

- Você pode se conectar a um container e executar comandos:

```
# Conectar no container terminal
docker exec -it <CONTAINER-NAME> /bin/sh

# Dentro do container você pode executar comandos:
ls
hostname
exit  # Para sair container terminal
```

- Você pode também executar comandos sem entrar no container:
```
# Listar:
docker exec -it myapp1 ls

# Pegar o hostname do container
docker exec -it myapp1 hostname

# Printar environment variables
docker exec -it myapp1 printenv

# Checar disk space usage:
docker exec -it myapp1 df -h
```

**Step 5: Stop e Start Docker Containers**

```
# Parar um running container
docker stop <CONTAINER-NAME>

# Testar se a aplicação caiu
curl http://localhost:8080a

# Start no stopped container
docker start <CONTAINER-NAME>

# Testar se a aplicação está no ar
curl http://localhost:8080
```

**Step 6: Remove Docker Containers**

```
# Stop no container 
docker stop <CONTAINER-NAME>
docker stop myapp1

# Remover o container
docker rm <CONTAINER-NAME>
docker rm myapp1

# Ou stop e remove o container em um comando
docker rm -f <CONTAINER-NAME>
docker rm -f myapp1
```

**Step 7: Remove Docker Images**

```
# Listar Docker images
docker images

# Remove Docker image usando Image ID
docker rmi <IMAGE-ID>

# Remove Docker image usando Image Name e Tag
docker rmi <IMAGE-NAME>:<IMAGE-TAG>

```




