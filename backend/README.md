# API JWT

Ejemplo de una Web API con FastAPI que emite JSON Web Tokens (JWT) para el
usuario `admin`. Los tokens expiran a los 300 segundos y pueden renovarse
mientras sigan vigentes.

## Requisitos

- Python 3.11+
- [Poetry](https://python-poetry.org/) o Docker

## Ejecución local

Desde la carpeta `backend`:

```bash
poetry install
export JWT_SECRET_KEY="una-clave-secreta-segura"
poetry run uvicorn app.main:app --reload
```

La documentación interactiva estará en <http://localhost:8000/docs>.

## Uso

Solicita un token con las credenciales `admin` / `admin123`:

```bash
curl -X POST http://localhost:8000/token \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"admin123"}'
```

La respuesta contiene `access_token`, `token_type` y `expires_in` (300).
Para renovarlo antes de que expire:

```bash
curl -X POST http://localhost:8000/token/refresh \
  -H 'Content-Type: application/json' \
  -d '{"token":"<access_token>"}'
```

## Docker

Desde `backend`, define una clave para entornos no locales y ejecuta:

```bash
export JWT_SECRET_KEY="una-clave-secreta-segura"
docker compose up --build
```

## Pruebas

```bash
poetry run pytest
```
