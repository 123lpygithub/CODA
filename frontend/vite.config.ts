import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd(), 'VITE_')
  const apiUrl = process.env.VITE_API_BASE_URL ?? env.VITE_API_BASE_URL
  if (command === 'build' && apiUrl?.trim()) {
    const parsed = new URL(apiUrl)
    if (!['http:', 'https:'].includes(parsed.protocol) || parsed.username || parsed.password || parsed.search || parsed.hash) {
      throw new Error('VITE_API_BASE_URL must be an HTTP(S) origin without credentials, query, or fragment.')
    }
    if (parsed.pathname !== '/') {
      throw new Error('VITE_API_BASE_URL must be the backend origin, e.g. https://api.example.org (without /api).')
    }
    if (mode === 'production' && (parsed.protocol !== 'https:' || ['localhost', '127.0.0.1', '[::1]'].includes(parsed.hostname))) {
      throw new Error('Production builds require a public HTTPS backend, or an empty VITE_API_BASE_URL for same-origin /api.')
    }
  }
  return {
    plugins: [react()],
    server: {
      port: 5173,
      strictPort: true,
    },
  }
})
