---
title: "Aprenda a Instrução USER no Dockerfile na Prática"
description: "Crie um Dockerfile com a instrução USER para executar aplicações como um usuário não-root."
---

# Aprenda a Instrução USER no Dockerfile na Prática

---

## Introdução

Neste guia, você irá:

- Criar uma aplicação Python Flask que exibe o usuário e grupo atual.
- Criar um Dockerfile que implementa a instrução `USER` para executar a aplicação como um usuário não-root.
- Construir a imagem Docker e verificar que a aplicação está sendo executada sob o usuário não-root especificado.

---

## Passo 1: Criar Aplicação Python de Exemplo e Dockerfile

### Criar uma Aplicação Python de Exemplo

**Nome do Arquivo:** `app.py`

```python
from flask import Flask
import os
import pwd
import grp

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Obter o ID e nome do usuário atual
    user_id = os.getuid()
    user_name = pwd.getpwuid(user_id).pw_name

    # Obter o ID e nome do grupo atual
    group_id = os.getgid()
    group_name = grp.getgrgid(group_id).gr_name

    # Retornar uma resposta exibindo o usuário e o grupo
    return f'Olá do usuário: {user_name} (UID: {user_id}) e grupo: {group_name} (GID: {group_id})!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Esta aplicação Flask exibirá o usuário e grupo atual quando acessada.

### Criar Dockerfile com a Instrução USER

**Dockerfile**

```dockerfile
# Use a imagem oficial do Python como base
FROM python

# Defina o diretório de trabalho dentro do container como /usr/src/app
WORKDIR /usr/src/app

# Copie o conteúdo do diretório atual no host para /usr/src/app no container
COPY *.py .

# Instale o pacote Flask usando pip
RUN pip install --no-cache-dir flask

# Defina variáveis de ambiente para o usuário e grupo não-root
ENV USER=mypythonuser
ENV GROUP=mypythongroup

# Crie um novo grupo 'mypygroup' e um usuário não-root 'mypythonuser' dentro deste grupo
RUN groupadd -r ${GROUP} && useradd -m -r -g ${GROUP} ${USER}

# Altere a propriedade do diretório /usr/src/app para o usuário não-root
RUN chown -R ${USER}:${GROUP} /usr/src/app

# Troque para o usuário não-root 'mypythonuser'
USER ${USER}

# Comando para executar a aplicação Python
CMD ["python", "app.py"]

# Exponha a porta 5000 para o host
EXPOSE 5000
```

**Explicação:**

- **FROM python**: Usa a imagem base do Python.
- **WORKDIR /usr/src/app**: Define o diretório de trabalho no container.
- **COPY app.py .**: Copia o código da aplicação para o container.
- **RUN pip install --no-cache-dir flask**: Instala o Flask sem cache para reduzir o tamanho da imagem.
- **ENV USER=mypythonuser** e **ENV GROUP=mypythongroup**: Define variáveis de ambiente para o usuário e grupo.
- **RUN groupadd** e **useradd**: Cria um grupo e um usuário não-root.
- **RUN chown**: Altera a propriedade do diretório para o usuário não-root.
- **USER ${USER}**: Troca para o usuário não-root.
- **EXPOSE 5000**: Exponha a porta 5000.
- **CMD ["python", "app.py"]**: Inicia a aplicação Flask.

---

## Passo 2: Construir a Imagem Docker e Executá-la

```bash
# Mude para o diretório que contém seu Dockerfile
cd DockerFiles

# Construa a imagem Docker
docker build -t demo13-dockerfile-user:v1 .

# Execute o container Docker
docker run --name my-user-demo -p 5000:5000 -d demo13-dockerfile-user:v1

# Liste os containers Docker
docker ps

# Saída Esperada:
# CONTAINER ID   IMAGE                       COMMAND             CREATED          STATUS          PORTS                    NAMES
# abcd1234efgh   demo13-dockerfile-user:v1   "python app.py"     10 seconds ago   Up 8 seconds    0.0.0.0:5000->5000/tcp   my-user-demo

# Acesse a aplicação no navegador
http://localhost:5000
```

**Saída Esperada no Navegador:**

```
Olá do usuário: mypythonuser (UID: 1000) e grupo: mypythongroup (GID: 1000)!
```

**Verificar Usuário e Grupo Dentro do Container:**

```bash
# Conecte-se ao container
docker exec -it my-user-demo /bin/bash

# Dentro do container, liste os arquivos e suas permissões
ls -l

# Saída Esperada:
# total 8
# -rw-r--r--    1 mypythonuser mypythongroup     629 Oct 13 12:00 app.py

# Verifique as variáveis de ambiente
env

# Procure pelas variáveis USER e GROUP
# USER=mypythonuser
# GROUP=mypythongroup

# Saia do shell do container
exit
```

---

## Passo 3: Como Conectar ao Container com Usuário Root?

```bash
# Conecte-se ao container como usuário root
docker exec --user root -it my-user-demo /bin/bash
```

**Nota:**

- Você será conectado ao container como usuário `root`.

---

## Passo 4: Parar e Remover Container e Imagens

```bash
# Pare e remova o container
docker rm -f my-user-demo

# Remova as imagens Docker da máquina local
docker rmi stacksimplify/demo13-dockerfile-user:v1
docker rmi demo13-dockerfile-user:v1

# Liste as imagens Docker para confirmar a remoção
docker images
```

---

## Conclusão

Você aprendeu a:

- Criar uma aplicação Python Flask que exibe o usuário e grupo atual.
- Criar um Dockerfile usando a instrução `USER` para executar a aplicação como um usuário não-root.
- Construir a imagem Docker e verificar que a aplicação está sendo executada sob o usuário não-root especificado.
- Marcar e enviar a imagem Docker para o Docker Hub.

---

## Notas Adicionais

- **Instrução USER:**

  - A instrução `USER` define o nome do usuário (ou UID) e, opcionalmente, o grupo (ou GID) a ser usado ao executar a imagem e para qualquer instrução `RUN`, `CMD` e `ENTRYPOINT` que a seguir no Dockerfile.

- **Melhores Práticas de Segurança:**

  - Executar aplicações como um usuário não-root dentro de containers Docker melhora a segurança.
  - Minimiza os danos potenciais caso o container seja comprometido.

- **Variáveis de Ambiente:**

  - Variáveis de ambiente definidas com a instrução `ENV` estão disponíveis durante o processo de build e em tempo de execução.
  - Podem ser acessadas no código da aplicação ou no shell do container.

---

## Recursos Adicionais

- [Documentação do Docker](https://docs.docker.com/)
- [Referência do Dockerfile - Instrução USER](https://docs.docker.com/engine/reference/builder/#user)
- [Melhores Práticas para Escrever Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Segurança no Docker - Executar como Usuário Não-Root](https://docs.docker.com/develop/security/#user)

---

**Feliz Dockerização!**