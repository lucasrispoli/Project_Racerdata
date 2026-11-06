# RacerData — Backend

API REST desenvolvida com **FastAPI** e **PostgreSQL**, rodando em **Docker**.

---

## Requisitos

- [Docker](https://www.docker.com/) instalado e em execução

---

## Como rodar

### 1. Derrubar os containers e volumes existentes

```bash
docker compose down -v
```

> ⚠️ O flag `-v` remove os volumes, incluindo os dados do banco. Use apenas quando quiser um ambiente limpo.

### 2. Subir os containers em background (com rebuild)

```bash
docker compose up -d --build
```

Isso irá:
- Construir a imagem da API
- Subir o container do **PostgreSQL**
- Subir o container da **API FastAPI**

### 3. Verificar se está rodando

```bash
docker compose ps
```

A API estará disponível em: [http://localhost:8080](http://localhost:8080)

Documentação interativa (Swagger): [http://localhost:8080/docs](http://localhost:8080/docs)

---

## Ver logs do backend

```bash
docker compose logs -f api
```

> Substitua `api` pelo nome do serviço definido no `docker-compose.yml` se for diferente.

---

## Parar os containers (sem remover dados)

```bash
docker compose down
```
