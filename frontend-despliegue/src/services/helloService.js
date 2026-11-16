/** Obtiene el saludo de la API, codificando el nombre como query string. */
export async function getHello(name = '') {
  const apiUrl = import.meta.env.VITE_API_URL
  if (!apiUrl) throw new Error('Falta configurar VITE_API_URL.')
  const url = new URL(`${apiUrl.replace(/\/$/, '')}/hello`)
  const cleanName = name.trim()
  if (cleanName) url.searchParams.set('name', cleanName)
  const response = await fetch(url, {
    headers: { Accept: 'application/json' },
    signal: AbortSignal.timeout(15000),
  })
  if (!response.ok) throw new Error(`Error ${response.status} al llamar a la API`)
  const data = await response.json()
  if (typeof data?.message !== 'string' || !data.message.trim()) {
    throw new Error('La API no ha devuelto un mensaje válido.')
  }
  return data.message
}
