




**Comandos básicos:**
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