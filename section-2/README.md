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
- Fazer o pullde docker images a partir do docker hub
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