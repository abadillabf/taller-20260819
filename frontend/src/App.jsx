import { useEffect, useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
const TOKEN_KEY = 'access_token'

function isWelcomePage() {
  return window.location.pathname === '/welcome'
}

function App() {
  const [token, setToken] = useState(() => sessionStorage.getItem(TOKEN_KEY))
  const [credentials, setCredentials] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    if (isWelcomePage() && !token) {
      window.history.replaceState({}, '', '/')
    }
  }, [token])

  function showWelcome() {
    window.history.pushState({}, '', '/welcome')
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setIsSubmitting(true)

    try {
      const response = await fetch(`${API_URL}/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      })
      const body = await response.json()

      if (!response.ok) {
        throw new Error(body.detail || 'No fue posible iniciar sesión.')
      }

      sessionStorage.setItem(TOKEN_KEY, body.access_token)
      setToken(body.access_token)
      showWelcome()
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : 'No fue posible conectar con el servidor.',
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  function handleLogout() {
    sessionStorage.removeItem(TOKEN_KEY)
    setToken(null)
    window.history.replaceState({}, '', '/')
  }

  if (isWelcomePage() && token) {
    return (
      <main className="page">
        <section className="card welcome-card" aria-labelledby="welcome-title">
          <span className="eyebrow">Sesión iniciada</span>
          <h1 id="welcome-title">¡Bienvenido!</h1>
          <p>Has accedido correctamente a la aplicación.</p>
          <button type="button" onClick={handleLogout}>
            Cerrar sesión
          </button>
        </section>
      </main>
    )
  }

  return (
    <main className="page">
      <section className="card" aria-labelledby="login-title">
        <span className="eyebrow">JWT API</span>
        <h1 id="login-title">Inicia sesión</h1>
        <p className="subtitle">Ingresa tus credenciales para continuar.</p>
        <form onSubmit={handleSubmit}>
          <label htmlFor="username">
            Usuario
            <input
              id="username"
              name="username"
              autoComplete="username"
              value={credentials.username}
              onChange={(event) =>
                setCredentials({ ...credentials, username: event.target.value })
              }
              required
            />
          </label>
          <label htmlFor="password">
            Contraseña
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              value={credentials.password}
              onChange={(event) =>
                setCredentials({ ...credentials, password: event.target.value })
              }
              required
            />
          </label>
          {error && <p className="error" role="alert">{error}</p>}
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Ingresando…' : 'Ingresar'}
          </button>
        </form>
      </section>
    </main>
  )
}

export default App
