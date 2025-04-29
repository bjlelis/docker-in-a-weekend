---
title: "Aprenda as Instruções ARG vs ENV, CMD, RUN, WORKDIR no Dockerfile na Prática"
description: "Entenda as diferenças entre as instruções ARG e ENV em Dockerfiles e aprenda a usar as instruções CMD, RUN e WORKDIR com exemplos práticos."
---

# Aprenda as Instruções ARG vs ENV, CMD, RUN, WORKDIR no Dockerfile na Prática

---

## Introdução

Neste guia, você irá:

1. Aprender as diferenças entre as instruções `ARG` e `ENV` em Dockerfiles.
2. Aprender a usar as instruções `CMD`, `RUN` e `WORKDIR`.
3. Criar uma aplicação simples em Python Flask.
4. Construir imagens Docker usando as instruções `ARG` e `ENV` para gerenciar variáveis de tempo de build e runtime.

---

## Por que Usar ARG e ENV Juntos?

- A instrução `ARG` permite passar variáveis no tempo de build sem modificar o Dockerfile, tornando-o mais dinâmico e reutilizável.
- Combinando `ARG` e `ENV`, você pode passar valores configurados durante o processo de build para o ambiente de runtime do container.
- **Separação de Responsabilidades:**
  - `ARG` é usado para personalização no **tempo de build**.
  - `ENV` é usado para personalização no **tempo de execução**.
- Essa separação torna o Dockerfile flexível em ambas as etapas, sem sobreposição ou confusão.

---

## Passo 1: Criar Aplicação em Python

**Crie o arquivo `requirements.txt`:**

```plaintext
Flask==3.0.3
```

**Crie uma pasta `templates`** com dois arquivos HTML: `dev.html` e `qa.html`.

**`templates/dev.html`:**

```html
<!DOCTYPE html>
<html>
  <body style="background-color: rgb(152, 202, 134);">
    <h1>Bem-vindo ao StackSimplify - Variáveis ARG (Build-time) e ENV (Runtime)</h1>
    <h2>Ambiente: DEV</h2>
    <p>Aprenda tecnologia por meio de demonstrações práticas e reais.</p>
    <p>Versão da Aplicação: V1</p>
  </body>
</html>
```

**`templates/qa.html`:**

```html
<!DOCTYPE html>
<html>
  <body style="background-color: rgb(134, 196, 202);">
    <h1>Bem-vindo ao StackSimplify - Variáveis ARG (Build-time) e ENV (Runtime)</h1>
    <h2>Ambiente: QA</h2>
    <p>Aprenda tecnologia por meio de demonstrações práticas e reais.</p>
    <p>Versão da Aplicação: V1</p>
  </body>
</html>
```

**Crie o arquivo `app.py`:**

```python
from flask import Flask, render_template
import os

app = Flask(__name__)

# Obtenha a variável de ambiente APP_ENVIRONMENT (padrão: 'dev')
environment = os.getenv('APP_ENVIRONMENT', 'dev')

@app.route('/')
def home():
    # Sirva templates diferentes com base no ambiente
    if environment == 'dev':
        return render_template('dev.html')
    elif environment == 'qa':
        return render_template('qa.html')
    else:
        return "<h1>Ambiente Desconhecido</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
```

---

## Passo 2: Criar Dockerfile com Instruções ARG e ENV

- **Diretório:** `Dockerfiles`

Crie um `Dockerfile` com o seguinte conteúdo:

```dockerfile
# Use python:3.12-alpine como imagem base
FROM python:3.12-alpine

# Labels OCI
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: ARG vs ENV no Docker"
LABEL org.opencontainers.image.description="Um exemplo de Dockerfile ilustrando a diferença entre as instruções ARG (build-time) e ENV (runtime)"
LABEL org.opencontainers.image.version="1.0"

# Defina um argumento de build para o ambiente (padrão: "dev")
ARG ENVIRONMENT=dev

# Configure a variável ENV usando o valor de ARG
ENV APP_ENVIRONMENT=${ENVIRONMENT}

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie os requisitos e instale as dependências
COPY requirements.txt requirements.txt

# Instale os pacotes do requirements.txt
RUN pip install -r requirements.txt

# Copie o código da aplicação
COPY app.py .

# Copie o diretório templates
COPY templates/ ./templates/

# Imprima o ambiente para fins de demonstração
RUN echo "Construindo para o ambiente: ${APP_ENVIRONMENT}"

# Exponha a porta 80
EXPOSE 80

# Inicie a aplicação Flask
CMD ["python", "app.py"]
```

---

## Passo 3: Construir Imagens Docker e Executá-las

### Construir Imagem Docker com Valor Padrão do ARG

```bash
# Mude para o diretório que contém seu Dockerfile
cd Dockerfiles

# Construa a imagem Docker usando o ENVIRONMENT padrão (dev)
docker build -t demo9-arg-vs-env:v1 .

# Execute o container Docker
docker run --name my-arg-env-demo1-dev -p 8080:80 -d demo9-arg-vs-env:v1

# Liste os containers Docker
docker ps

# Imprima as variáveis de ambiente do container
docker exec -it my-arg-env-demo1-dev env | grep APP_ENVIRONMENT

# Saída Esperada:
# APP_ENVIRONMENT=dev

# Acesse a aplicação no navegador
http://localhost:8080
```

**Saída Esperada:**

- A página HTML **Dev** deve ser exibida, indicando que o `APP_ENVIRONMENT` está configurado como `dev`.

### Executar Container Docker e Substituir Variável ENV

```bash
# Execute o container Docker e substitua APP_ENVIRONMENT para 'qa'
docker run --name my-arg-env-demo2-qa -p 8081:80 -e APP_ENVIRONMENT=qa -d demo9-arg-vs-env:v1

# Liste os containers Docker
docker ps

# Imprima as variáveis de ambiente do container
docker exec -it my-arg-env-demo2-qa env | grep APP_ENVIRONMENT

# Saída Esperada:
# APP_ENVIRONMENT=qa

# Acesse a aplicação no navegador
http://localhost:8081
```

**Saída Esperada:**

- A página HTML **QA** deve ser exibida, indicando que o `APP_ENVIRONMENT` foi substituído para `qa` em tempo de execução.

---

## Passo 4: Verificar Instruções WORKDIR e CMD

**Verificar WORKDIR:**

```bash
# Liste os arquivos no diretório de trabalho dentro do container
docker exec -it my-arg-env-demo1-dev ls /app

# Saída Esperada:
# app.py
# requirements.txt
# templates
```

- Os arquivos `app.py`, `requirements.txt` e o diretório `templates` devem estar presentes no diretório `/app` dentro do container, confirmando que a instrução `WORKDIR` está funcionando como esperado.

**Verificar CMD:**

```bash
# Inspecione a imagem Docker para verificar a instrução CMD
docker image inspect demo9-arg-vs-env:v1 --format='{{.Config.Cmd}}'

# Saída Esperada:
# [python app.py]
```

- Isso confirma que a instrução `CMD` está configurada para iniciar a aplicação Flask usando `python app.py`.

---

## Passo 5: Configurar Ambiente Padrão como QA Sem Alterar o Dockerfile

**Pergunta:** Como garantir que o ambiente padrão seja `qa` ao construir a imagem Docker sem alterar o Dockerfile?

**Resposta:**

Você pode substituir o argumento de build `ENVIRONMENT` durante o processo de construção da imagem usando a flag `--build-arg`. Isso permite configurar o `APP_ENVIRONMENT` padrão como `qa` na imagem sem modificar o Dockerfile.

```bash
# Construa a imagem Docker com ENVIRONMENT configurado como 'qa'
docker build --build-arg ENVIRONMENT=qa -t demo9-arg-vs-env:v1-qa .

# Execute o container Docker sem especificar a variável de ambiente
docker run --name my-arg-env-demo3-qa -p 8082:80 -d demo9-arg-vs-env:v1-qa

# Liste os containers Docker
docker ps

# Imprima as variáveis de ambiente do container
docker exec -it my-arg-env-demo3-qa env | grep APP_ENVIRONMENT

# Saída Esperada:
# APP_ENVIRONMENT=qa

# Acesse a aplicação no navegador
http://localhost:8082
```

**Explicação:**

- Passando `--build-arg ENVIRONMENT=qa`, você configura o argumento de build `ARG ENVIRONMENT` como `qa`.
- A instrução `ENV APP_ENVIRONMENT=${ENVIRONMENT}` define `APP_ENVIRONMENT` como `qa` na imagem.
- Quando você executa o container, `APP_ENVIRONMENT` já está configurado como `qa` por padrão, sem necessidade de passar `-e APP_ENVIRONMENT=qa`.
- A aplicação servirá a página HTML **QA** sem configurações adicionais em tempo de execução.

**Limpeza:**

```bash
# Pare e remova o container
docker rm -f my-arg-env-demo3-qa

# Remova a imagem Docker
docker rmi demo9-arg-vs-env:v1-qa
```

---

## Conclusão

Você aprendeu a:

- Entender as diferenças entre as instruções `ARG` e `ENV` em Dockerfiles.
- Criar um Dockerfile que usa as instruções `ARG`, `ENV`, `CMD`, `RUN` e `WORKDIR`.
- Construir imagens Docker com valores padrão e substituídos sem modificar o Dockerfile.
- Executar containers Docker e verificar as configurações de ambiente.
- Verificar a funcionalidade das instruções `WORKDIR` e `CMD`.
- Marcar e enviar imagens Docker para o Docker Hub.

---

## Notas Adicionais

- **ARG vs. ENV:**
  - **ARG** é usado para variáveis de tempo de build e não está disponível após a construção da imagem.
  - **ENV** define variáveis de ambiente disponíveis durante o processo de build e no container em execução.

- **Substituir Variáveis ENV:**
  - Você pode substituir variáveis `ENV` em tempo de execução usando a flag `-e` com `docker run`.

- **Instrução CMD:**
  - A instrução `CMD` especifica o comando padrão a ser executado ao iniciar um container a partir da imagem.
  - Pode ser substituída especificando um comando diferente em `docker run`.

- **Instrução WORKDIR:**
  - A instrução `WORKDIR` define o diretório de trabalho para qualquer instrução `RUN`, `CMD`, `ENTRYPOINT`, `COPY` e `ADD` que a seguir no Dockerfile.
  - Garante que os arquivos da aplicação estejam localizados em um local previsível dentro do container.

- **Melhores Práticas:**
  - Use `ARG` para valores que você pode querer alterar durante o build sem modificar o Dockerfile.
  - Use `ENV` para definir valores padrão que podem ser substituídos em tempo de execução, se necessário.
  - Mantenha suas imagens Docker leves, minimizando o número de camadas e removendo arquivos desnecessários.

---

## Recursos Adicionais

- [Documentação do Docker](https://docs.docker.com/)
- [Referência do Dockerfile - Instrução ARG](https://docs.docker.com/engine/reference/builder/#arg)
- [Referência do Dockerfile - Instrução ENV](https://docs.docker.com/engine/reference/builder/#env)
- [Referência do Dockerfile - Instrução CMD](https://docs.docker.com/engine/reference/builder/#cmd)
- [Referência do Dockerfile - Instrução WORKDIR](https://docs.docker.com/engine/reference/builder/#workdir)
- [Entendendo ARG e ENV no Dockerfile](https://vsupalov.com/docker-arg-vs-env/)
- [Melhores Práticas para Escrever Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

**Feliz Dockerização!**