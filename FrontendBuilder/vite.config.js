import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    plugins: [vue()],
    build: {
        rollupOptions: {
            output: {
                manualChunks(id) {
                    if (id.includes('node_modules')) {
                        if (id.includes('@auth0')) return 'auth-vendor';
                        if (id.includes('axios')) return 'network-vendor';
                        return 'vendor';
                    }
                }
            }
        }
    }
})