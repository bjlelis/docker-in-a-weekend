---
title: "Aprenda as Instruções ADD vs COPY no Dockerfile na Prática"
description: "Crie um Dockerfile com as instruções ADD e COPY para entender suas diferenças na construção de imagens Docker."
---

# Aprenda as Instruções ADD vs COPY no Dockerfile na Prática

---

## Introdução

Neste guia, você irá:

- Criar um Dockerfile do Nginx usando `nginx:alpine-slim` como imagem base.
- Adicionar labels à sua imagem Docker.
- Adicionar as instruções `COPY` e `ADD` no Dockerfile e entender as diferenças.
- Construir a imagem Docker.
- Enviar a imagem Docker para o Docker Hub.

---

## Passo 1: Criar um Repositório no GitHub

## Passo 2: Revisar a Pasta App-Files e Compactar os Arquivos

```bash
# Navegue até o diretório App-Files
cd App-Files

# Crie um arquivo tar.gz com os arquivos
tar -czvf static_files.tar.gz index.html file1.html file2.html file3.html file4.html file5.html

# Copie o arquivo tar.gz para o diretório Dockerfiles
cp static_files.tar.gz ../Dockerfiles

# Revise o arquivo copy-file.html no diretório Dockerfiles
cat ../Dockerfiles/copy-file.html
```

---

## Passo 3: Criar Dockerfile e Copiar Arquivos Personalizados

- **Pasta:** Dockerfiles

Crie um `Dockerfile` com o seguinte conteúdo:

```dockerfile
# Use nginx:alpine-slim como imagem base do Docker
FROM nginx:alpine-slim

# Labels OCI
LABEL org.opencontainers.image.authors="Kalyan Reddy Daida"
LABEL org.opencontainers.image.title="Demo: COPY vs ADD Instructions in Dockerfile"
LABEL org.opencontainers.image.description="Um exemplo de Dockerfile ilustrando as diferenças entre as instruções COPY e ADD, incluindo a cópia de arquivos e extração de tarballs."
LABEL org.opencontainers.image.version="1.0"

# Usando COPY para copiar um arquivo local
COPY copy-file.html /usr/share/nginx/html

# Usando ADD para copiar um arquivo e extrair um tarball
ADD static_files.tar.gz /usr/share/nginx/html
```

---

## Passo 4: Construir a Imagem Docker e Executá-la

```bash
# Mude para o diretório Dockerfiles
cd Dockerfiles

# Construa a imagem Docker
docker build -t [IMAGE-NAME]:[IMAGE-TAG] .

# Exemplo:
docker build -t demo5-dockerfile-add-vs-copy:v1 .

# Execute o container Docker e verifique
docker run --name my-add-vs-copy-demo -p 8080:80 -d demo5-dockerfile-add-vs-copy:v1

# Liste os arquivos estáticos no container Docker
docker exec -it my-add-vs-copy-demo ls -lrta /usr/share/nginx/html

# Acesse a aplicação
http://localhost:8080
```

---

## Passo 5: Parar e Remover Container e Imagens

```bash
# Pare e remova o container
docker rm -f my-add-vs-copy-demo

# Remova as imagens Docker
docker rmi stacksimplify/demo5-dockerfile-add-vs-copy:v1
docker rmi demo5-dockerfile-add-vs-copy:v1

# Liste as imagens Docker para confirmar a remoção
docker images
```

---

## Passo 6: COPY vs ADD no Dockerfile

Ao trabalhar com Dockerfiles, é importante entender a diferença entre as instruções `COPY` e `ADD`. Ambas são usadas para copiar arquivos do host para a imagem Docker, mas possuem comportamentos distintos e melhores práticas.

### Pontos-Chave:

1. **COPY**:
   - Copia arquivos e diretórios do contexto de build para a imagem.
   - Simples e explícito em sua funcionalidade, usado apenas para transferências de arquivos.
   - Preferido para arquivos e diretórios locais, pois é mais rápido e evita efeitos colaterais indesejados.

2. **ADD**:
   - Faz tudo o que o `COPY` faz, mas com recursos adicionais.
   - Extrai automaticamente arquivos tar (ex.: `.tar`, `.tar.gz`).
   - Suporta URLs, permitindo baixar arquivos da web.
   - Mais versátil, mas pode introduzir riscos de segurança (especialmente com URLs) e comportamentos indesejados (ex.: extração automática).

### Melhor Prática:

- Use `COPY` sempre que possível para arquivos locais. Reserve `ADD` para casos em que você precise extrair um tarball ou baixar de uma URL.

### Tabela Comparativa:

| Recurso                   | `COPY`                                   | `ADD`                                          |
|---------------------------|------------------------------------------|------------------------------------------------|
| **Transferência de Arquivos** | Copia arquivos do contexto de build       | Copia arquivos do contexto de build            |
| **Extração de Arquivos Tar** | Não                                      | Sim (extrai automaticamente arquivos `.tar`)   |
| **Suporte a URLs**        | Não                                      | Sim (pode baixar arquivos da web)              |
| **Desempenho**            | Mais rápido, menos sobrecarga            | Pode ser mais lento ao usar recursos adicionais|
| **Segurança**             | Mais seguro para transferências locais   | Pode introduzir riscos ao baixar de URLs       |
| **Caso de Uso**           | Preferido para cópias locais             | Use apenas para extração de tar ou download de URLs |

---

## Conclusão

Você aprendeu a:

- Criar um Dockerfile usando `nginx:alpine-slim` como imagem base.
- Usar as instruções `COPY` e `ADD` no Dockerfile para entender suas diferenças.
  - `COPY` é usado para copiar arquivos e diretórios.
  - `ADD` também copia arquivos, mas possui recursos adicionais, como extração de arquivos compactados e suporte a URLs remotas.
- Construir e executar uma imagem Docker.
- Enviar a imagem Docker para o Docker Hub.

---

## Notas Adicionais

- **Substitua os Marcadores:** Lembre-se de substituir `[IMAGE-NAME]`, `[IMAGE-TAG]`, `[DOCKER_USERNAME]` e outros marcadores pelos seus valores reais.
- **Melhores Práticas:**
  - Use tags explícitas para suas imagens Docker para gerenciar versões de forma eficaz.
  - Limpe imagens e containers não utilizados para liberar espaço em disco.

---

## Recursos Adicionais

- [Documentação do Docker](https://docs.docker.com/)
- [Referência do Dockerfile](https://docs.docker.com/engine/reference/builder/)
- [Melhores Práticas para Escrever Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Entendendo COPY vs. ADD no Dockerfile](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#add-or-copy)

---

**Feliz Dockerização!**