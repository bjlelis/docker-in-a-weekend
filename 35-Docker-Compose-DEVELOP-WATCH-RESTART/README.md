---
title: "Domine o recurso Develop Watch do Docker Compose para um Desenvolvimento Eficiente"
description: "Aprenda a usar o recurso Develop Watch do Docker Compose para melhorar seu fluxo de trabalho de desenvolvimento com sincronização de código ao vivo e reinicializações automáticas de containers."
---

# Domine o recurso Develop Watch do Docker Compose para um Desenvolvimento Eficiente

---

## Step-01: Introdução

Neste guia, você aprenderá a usar o recurso **Develop Watch** do Docker Compose para melhorar seu fluxo de trabalho de desenvolvimento. Este recurso permite:

- **Sincronizar alterações** no seu código em tempo real sem reconstruir imagens.
- **Reiniciar automaticamente** containers quando arquivos de configuração forem alterados.
- Usar a opção `--watch` para habilitar o recurso Develop Watch.

---

## Step-02: Revisar o Dockerfile

**Local do Arquivo:** `sync-and-restart-demo/web/Dockerfile`

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

- `sync-and-restart-demo/web/html/index.html`
- `sync-and-restart-demo/web/html/custom_404.html`

### Configuração do NGINX

**Local do Arquivo:** `sync-and-restart-demo/web/nginx.conf`

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

    # Página 404 personalizada - HABILITE as 5 linhas abaixo para testar a opção "sync+restart" no Docker Compose
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

**Local do Arquivo:** `sync-and-restart-demo/docker-compose.yaml`

```yaml
services:
  web:
    container_name: mywebserver1
    build:
      context: ./web  # Caminho para o Dockerfile
      dockerfile: Dockerfile  # Dockerfile a ser usado para construir a imagem
    develop:
      watch: 
        # Sincronizar alterações no conteúdo estático
        - path: ./web/html
          action: sync
          target: /usr/share/nginx/html 
        # Sincronizar alterações no arquivo nginx.conf
        - path: ./web/nginx.conf
          action: sync+restart
          target: /etc/nginx/nginx.conf     
    ports:
      - "8080:8080" 
```

---

## Step-05: Iniciar a Pilha e Verificar

Use a opção `--watch` para habilitar o recurso Develop Watch.

```bash
# Alterar para o diretório do projeto
cd sync-and-restart-demo

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

**Local do Arquivo:** `sync-and-restart-demo/web/html/index.html`

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

Antes de testar a opção `sync+restart`, verifique a página 404 padrão.

```bash
# Acessar uma página inexistente para testar a página 404
http://localhost:8080/abc

# Observação:
# A página 404 padrão do NGINX será exibida.
```

---

## Step-08: Testar a Opção Sync + Restart: Atualizar `nginx.conf`

### Step-08-01: Habilitar Página 404 Personalizada em `nginx.conf`

Descomente as seguintes linhas em `nginx.conf`:

```conf
    # Página 404 personalizada - HABILITE as 5 linhas abaixo para testar a opção "sync+restart" no Docker Compose
    error_page 404 /custom_404.html;
    location = /custom_404.html {
      root /usr/share/nginx/html;  # Localização da página 404 personalizada
      internal;
    }    
```

### Step-08-02: Verificar Reinício Automático do Container

```bash
# Listar containers
docker ps

# Acessar uma página inexistente para testar a página 404 personalizada
http://localhost:8080/abc

# Observação:
# - A página 404 personalizada do NGINX será exibida.
# - A ação 'sync+restart' definida no arquivo Docker Compose sincronizou o arquivo 'nginx.conf' atualizado com o container e o reiniciou automaticamente para aplicar as alterações.
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

Neste tutorial, você aprendeu a aproveitar o recurso **Develop Watch** do Docker Compose para melhorar seu fluxo de trabalho de desenvolvimento. Configurando a opção `watch` no seu arquivo `docker-compose.yaml`, você pode:

- **Sincronizar automaticamente** alterações no código da aplicação ou arquivos estáticos para containers em execução.
- **Reiniciar containers** automaticamente quando arquivos de configuração forem alterados, garantindo que as atualizações sejam aplicadas sem intervenção manual.

Este recurso acelera significativamente os ciclos de desenvolvimento, eliminando a necessidade de reconstruir imagens ou reiniciar containers manualmente para cada alteração.

---

## Notas Adicionais

- **Sync vs. Sync + Restart**:
  - **Sync**: Atualiza arquivos dentro do container sem reiniciá-lo. Ideal para conteúdo estático ou código que não requer reinício.
  - **Sync + Restart**: Atualiza arquivos e reinicia o container. Use isso quando alterações exigirem um reinício do serviço para entrar em vigor (por exemplo, arquivos de configuração).

- **Desenvolvimento Eficiente**:
  - O recurso Develop Watch é especialmente útil para desenvolvimento e testes rápidos, permitindo que os desenvolvedores vejam alterações em tempo real.

- **Limitações**:
  - Este recurso é destinado a ambientes de desenvolvimento e deve ser usado com cautela em configurações de produção.

---

## Recursos Adicionais

- [Documentação do Docker Compose](https://docs.docker.com/compose/)
- [Seção Develop do Docker Compose](https://docs.docker.com/compose/reference/develop/)
- [Documentação Oficial do NGINX](https://nginx.org/en/docs/)
- [Live Reloading com Docker](https://docs.docker.com/compose/develop/)

---

**Feliz Dockerização!**