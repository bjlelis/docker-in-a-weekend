---
title: "Domine o recurso Develop Watch do Docker Compose com a opção Rebuild"
description: "Aprenda a usar o recurso Develop Watch do Docker Compose para melhorar seu fluxo de trabalho de desenvolvimento com sincronização de código ao vivo e builds automáticos de imagens Docker."
---

# Domine o recurso Develop Watch do Docker Compose com Builds Automáticos de Imagens Docker

---

## Step-01: Introdução

Neste guia, você aprenderá a usar o recurso **Develop Watch** do Docker Compose com a opção rebuild para melhorar seu fluxo de trabalho de desenvolvimento. Este recurso permite:

- **Sincronizar alterações** no seu código em tempo real sem reconstruir imagens.
- **Reconstruir automaticamente imagens Docker** quando alterações ocorrerem em arquivos de configuração monitorados.

---

## Step-02: Revisar o Dockerfile

**Local do Arquivo:** `sync-and-rebuild-demo/web/Dockerfile`

```dockerfile
# Usar a imagem base oficial do NGINX
FROM nginx:latest

# Copiar o arquivo de configuração personalizado do NGINX para substituir o default.conf
COPY ./nginx.conf /etc/nginx/nginx.conf

# Copiar arquivos do site estático para o diretório HTML do container
COPY ./html /usr/share/nginx/html

# Expor a porta 8080 para acesso externo
EXPOSE 8080

# Iniciar o NGINX
CMD ["nginx", "-g", "daemon off;"]
```

---

## Step-03: Revisar Outros Arquivos

### Arquivos HTML

- `sync-and-rebuild-demo/web/html/index.html`
- `sync-and-rebuild-demo/web/html/custom_404.html`

### Configuração do NGINX

**Local do Arquivo:** `sync-and-rebuild-demo/web/nginx.conf`

```conf
events { }

http {
  server {
    listen 8080;

    # Servir arquivos do diretório raiz html para '/'
    location / {
      root /usr/share/nginx/html;  # Servir arquivos estáticos deste diretório
      index index.html;  # Servir index.html por padrão, se existir
    }

    # Página 404 personalizada - HABILITE as 5 linhas abaixo para testar a opção "sync+rebuild" no Docker Compose
    # error_page 404 /custom_404.html;
    # location = /custom_404.html {
    #   root /usr/share/nginx/html;  # Localização da página 404 personalizada
    #   internal;
    # }    

  }
}
```

---

## Step-04: Revisar `docker-compose.yaml`

**Local do Arquivo:** `sync-and-rebuild-demo/docker-compose.yaml`

```yaml
services:
  web:
    container_name: mywebserver2
    build:
      context: ./web  # Caminho para o Dockerfile
      dockerfile: Dockerfile  # Dockerfile a ser usado para construir a imagem
    develop:
      watch: 
        # Sincronizar alterações no conteúdo estático
        - path: ./web/html
          action: sync
          target: /usr/share/nginx/html 
        # Reconstruir a imagem quando nginx.conf for alterado
        - path: ./web/nginx.conf
          action: rebuild
          target: /etc/nginx/nginx.conf     
    ports:
      - "8080:8080" 
```

---

## Step-05: Iniciar a Pilha e Verificar

Use a opção `--watch` para habilitar o recurso Develop Watch.

```bash
# Alterar para o diretório do projeto
cd sync-and-rebuild-demo

# Baixar imagens Docker e iniciar os containers com a opção --watch
docker compose up --watch 

# Listar containers Docker
docker compose ps

# Acessar a aplicação
http://localhost:8080

# Observação:
# A versão V1 da aplicação será exibida.
```

---

## Step-06: Testar a Opção Sync: Atualizar `index.html` para a Versão 2

**Local do Arquivo:** `sync-and-rebuild-demo/web/html/index.html`

Atualize o conteúdo:

```html
<p>Application Version: V2</p>
```

**Observação:**

- Alterações no conteúdo estático serão sincronizadas automaticamente com o container.
- Você verá a versão V2 da aplicação sem reiniciar o container.

```bash
# Acessar a aplicação
http://localhost:8080

# Observação:
# A versão V2 da aplicação será exibida.
```

---

## Step-07: Testar a Página 404 Padrão do NGINX

Antes de testar a opção `rebuild`, verifique a página 404 padrão.

```bash
# Acessar uma página inexistente para testar a página 404
http://localhost:8080/abc

# Observação:
# A página 404 padrão do NGINX será exibida.
```

---

## Step-08: Testar a Opção Rebuild: Atualizar `nginx.conf`

### Step-08-01: Habilitar Página 404 Personalizada em `nginx.conf`

Descomente as seguintes linhas em `nginx.conf`:

```conf
    # Página 404 personalizada - HABILITE as 5 linhas abaixo para testar a opção "sync+rebuild" no Docker Compose
    error_page 404 /custom_404.html;
    location = /custom_404.html {
      root /usr/share/nginx/html;  # Localização da página 404 personalizada
      internal;
    }    
```

### Step-08-02: Verificar se a Imagem Docker foi Reconstruída e Novo Container Criado

```bash
# Listar imagens Docker
docker images

# Observação:
# 1. Você verá uma nova imagem Docker criada após as alterações em 'nginx.conf'.
# 2. A ação 'rebuild' definida no arquivo Docker Compose reconstruiu a imagem Docker quando 'nginx.conf' foi atualizado.

# Listar containers
docker ps

# Acessar uma página inexistente para testar a página 404 personalizada
http://localhost:8080/abc

# Observação:
# - A página 404 personalizada do NGINX será exibida.
```

---

## Step-09: Limpeza

```bash
# Parar e remover containers
docker compose down

# Excluir imagens Docker (Opcional)
docker rmi $(docker images -q)
```

---

## Conclusão

Neste tutorial, você aprendeu a aproveitar o recurso **Develop Watch** do Docker Compose com a opção rebuild para melhorar seu fluxo de trabalho de desenvolvimento. Configurando a opção `watch` no seu arquivo `docker-compose.yaml`, você pode:

- **Sincronizar automaticamente** alterações no código da aplicação ou arquivos estáticos para containers em execução.
- **Reconstruir automaticamente imagens Docker** quando arquivos de configuração específicos forem alterados, garantindo que as atualizações sejam aplicadas e os containers sejam recriados com a nova imagem.

Este recurso acelera significativamente os ciclos de desenvolvimento, eliminando a necessidade de reconstruir imagens ou reiniciar containers manualmente para cada alteração.

---

## Notas Adicionais

- **Sync vs. Rebuild**:
  - **Sync**: Atualiza arquivos dentro do container sem reconstruir a imagem. Ideal para conteúdo estático ou código que não requer rebuild.
  - **Rebuild**: Reconstrói a imagem Docker quando arquivos especificados são alterados. Use isso quando alterações exigirem um novo build da imagem para entrar em vigor (por exemplo, alterações no `Dockerfile` ou arquivos de configuração copiados durante o build).

- **Desenvolvimento Eficiente**:
  - O recurso Develop Watch com a opção rebuild é especialmente útil para ambientes de desenvolvimento onde alterações de configuração são frequentes.

- **Limitações**:
  - Este recurso é destinado a ambientes de desenvolvimento e pode não ser adequado para configurações de produção devido ao overhead de reconstruir imagens frequentemente.

---

## Recursos Adicionais

- [Documentação do Docker Compose](https://docs.docker.com/compose/)
- [Seção Develop do Docker Compose](https://docs.docker.com/compose/reference/develop/)
- [Documentação Oficial do NGINX](https://nginx.org/en/docs/)
- [Live Reloading com Docker](https://docs.docker.com/compose/develop/)

---

**Feliz Dockerização!**