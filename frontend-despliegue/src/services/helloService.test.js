import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { getHello } from './helloService'

beforeEach(() => vi.stubEnv('VITE_API_URL', 'http://localhost:8000/api'))
afterEach(() => { vi.unstubAllGlobals(); vi.unstubAllEnvs() })

it.each(['', '   ', 'Ana', ' Ana García ', 'Ana & Luis'])('codifica el nombre %j', async (name) => {
  const message = `Hello World${name.trim() ? ` ${name.trim()}` : ''}`
  const mock = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ message }) })
  vi.stubGlobal('fetch', mock)
  expect(await getHello(name)).toBe(message)
  const [url, options] = mock.mock.calls[0]
  expect(url.pathname).toBe('/api/hello')
  expect(url.searchParams.get('name')).toBe(name.trim() || null)
  expect([...url.searchParams.keys()]).toEqual(name.trim() ? ['name'] : [])
  expect(options.headers.Accept).toBe('application/json')
})
it('gestiona errores HTTP', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 500 }))
  await expect(getHello()).rejects.toThrow('Error 500')
})
it('propaga errores de red', async () => {
  vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')))
  await expect(getHello()).rejects.toThrow('Failed to fetch')
})
it.each([{}, { message: 42 }, { message: '' }, null])('rechaza respuesta inválida %j', async (data) => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, json: async () => data }))
  await expect(getHello()).rejects.toThrow('mensaje válido')
})
it('detecta configuración ausente', async () => {
  vi.stubEnv('VITE_API_URL', '')
  await expect(getHello()).rejects.toThrow('VITE_API_URL')
})
