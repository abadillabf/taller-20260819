# Taller 20260819

Aplicación de ejemplo con una API FastAPI de autenticación JWT y un cliente React.

## Backend

Consulta [backend/README.md](backend/README.md) para instalar, configurar y ejecutar
la API. Al ejecutarla localmente queda disponible en `http://localhost:8000`.

## Frontend

La aplicación React muestra un formulario de inicio de sesión y una página de
bienvenida protegida. El token emitido por `POST /token` se conserva en
`sessionStorage`, por lo que la bienvenida (`/welcome`) no está disponible sin
una sesión iniciada.

Desde la raíz del proyecto:

```bash
cd frontend
npm install
npm run dev
```

Abre la dirección mostrada por Vite (normalmente `http://localhost:5173`). El
frontend usa `http://localhost:8000` como API predeterminada. Para otra URL,
crea `frontend/.env.local` con:

```bash
VITE_API_URL=http://localhost:8000
```

Si el frontend se sirve desde otro origen, configura el backend antes de
iniciarlo:

```bash
export FRONTEND_ORIGINS="http://localhost:5173"
```

Usa las credenciales definidas por `ADMIN_USERNAME` y `ADMIN_PASSWORD` al
iniciar el backend. Para la configuración de ejemplo son `admin` y `admin123`.
