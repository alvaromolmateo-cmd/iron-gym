import { defineConfig } from 'vite'

export default defineConfig({
  // Lee las variables VITE_* del .env de la raíz del repositorio
  envDir: '..',
  server: {
    host: true,
    port: 5173,
  },
})
