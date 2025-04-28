---
title: Install Docker Desktop 
description: Install Docker Desktop 
---

## Step-01: Introduction
1. Install Docker Desktop

## Step-02: Docker Desktop - Pricing, SignUp, Download
- [Docker Desktop Pricing](https://www.docker.com/pricing/)
- [SignUp Docker Hub](https://hub.docker.com/)
- [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

---

# Docker:

- Docker é uma ferramenta que permite criar, executar e gerenciar contêineres. Um contêiner é como uma "caixa leve" que contém tudo que a aplicação precisa: código, bibliotecas, dependências e configurações — tudo isolado do sistema operacional da máquina host.


**Imagem vs Contêiner**
- Imagem: É o "molde" de um contêiner. Contém o sistema de arquivos, bibliotecas e dependências da aplicação.
- Contêiner: É uma instância em execução de uma imagem.

**Principais comandos do Docker**

- docker build -t nome-imagem .     # Cria uma imagem a partir de um Dockerfile
- docker run nome-imagem            # Roda um contêiner a partir da imagem
- docker ps                         # Lista contêineres em execução
- docker ps -a                      # Lista todos os contêineres (mesmo parados)
- docker images                     # Lista imagens disponíveis
- docker stop id_ou_nome            # Para um contêiner
- docker rm id_ou_nome              # Remove um contêiner
- docker rmi nome-imagem            # Remove uma imagem

**Dockerfile**
- É um arquivo de texto com instruções para montar uma imagem. Exemplo básico:

```Dockerfile

FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "index.js"]```

**Docker Hub**
É o repositório público onde você pode buscar ou publicar imagens Docker, como o GitHub é para código.

Exemplo:

- docker pull nginx            # Baixa a imagem oficial do Nginx
- docker push usuario/imagem   # Envia sua imagem para o Docker Hub

**Docker Compose**
Ferramenta para definir e rodar múltiplos contêineres com um só comando. Usa um arquivo docker-compose.yaml para configurar serviços (como banco + backend + frontend).

**Volumes**
São usados para persistir dados fora do contêiner, evitando perda de dados ao reiniciar.

docker volume create meu-volume
docker run -v meu-volume:/app/data nome-imagem

**Portas**
Você pode mapear portas do host para o contêiner:

docker run -p 8080:80 nginx     # Isso expõe a porta 80 do contêiner na 8080 do seu computador

**Benefícios do Docker**
- Reprodutibilidade do ambiente
- Portabilidade
- Isolamento
- Escalabilidade
- Integração fácil com CI/CD

**Características-chave:**
- Imagens imutáveis: Uma vez criada, uma imagem não muda — o que garante consistência.
- Contêineres leves: Iniciam rapidamente e usam poucos recursos.
- Infraestrutura como código: Com Dockerfile, seu ambiente pode ser versionado.
- Fácil integração com orquestradores: Como Kubernetes.

---

## Docker dentro do DevSecOps:

O DevSecOps promove a inclusão de segurança desde o início do ciclo de desenvolvimento (shift-left). O Docker ajuda nisso de várias maneiras:

**Imagens seguras:**
- Verifique a base da imagem (FROM ubuntu:latest pode ser perigoso).
- Use imagens mínimas e oficiais sempre que possível (FROM alpine, node:slim, etc).
- Ferramentas como Trivy, Clair, Anchore fazem análise de vulnerabilidades em imagens Docker.

**Scan automatizado em pipelines CI/CD:**
- Docker permite escanear imagens automaticamente em pipelines (GitLab CI, GitHub Actions, Jenkins).
- Com isso, vulnerabilidades são detectadas antes do deploy.

**Controle de dependências:**
- Um Dockerfile define dependências fixas.
- Isso evita surpresas com atualizações de pacotes durante o build.

**Isolamento e segurança de execução:**
- Contêineres isolam processos da aplicação.
- Com boas práticas (usuário não-root, volumes seguros), o risco de escape é minimizado.

RUN adduser --disabled-password appuser   # Exemplo de boas práticas
USER appuser

**Compliance e auditoria:**
- Imagens são versionadas e podem ser assinadas com Docker Content Trust (DCT).
- Repositórios privados (Docker Hub, Harbor, Amazon ECR) podem impor políticas de segurança.

**Hardening:**
- Imagens são versionadas e podem ser assinadas com Docker Content Trust (DCT).
- Repositórios privados (Docker Hub, Harbor, Amazon ECR) podem impor políticas de segurança.

**Integração com orquestradores (ex: Kubernetes)**
- Kubernetes + Docker (ou containerd) permite aplicar políticas de segurança com ferramentas como: OPA Gatekeeper (políticas de admissão), PodSecurity Standards e NetworkPolicies


