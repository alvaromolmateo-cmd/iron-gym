import './style.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const app = document.querySelector('#app')
app.innerHTML = `
  <main class="card">
    <h1>Iron Gym</h1>
    <p>Comprobación de conexión con el backend</p>
    <p class="estado" id="estado">Consultando <code>${API_URL}/health</code>…</p>
    <pre id="respuesta" hidden></pre>
    <button id="reintentar" type="button">Volver a comprobar</button>
  </main>
`

const estado = document.querySelector('#estado')
const respuesta = document.querySelector('#respuesta')

async function comprobarBackend() {
  estado.className = 'estado'
  estado.textContent = 'Consultando el backend…'
  respuesta.hidden = true
  try {
    const res = await fetch(`${API_URL}/health`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const datos = await res.json()
    estado.classList.add('ok')
    estado.textContent = `Backend conectado: ${datos.status}`
    respuesta.textContent = JSON.stringify(datos, null, 2)
    respuesta.hidden = false
  } catch (error) {
    estado.classList.add('error')
    estado.textContent = `No se pudo conectar con ${API_URL}/health (${error.message})`
  }
}

document.querySelector('#reintentar').addEventListener('click', comprobarBackend)
comprobarBackend()
