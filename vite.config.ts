import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA, VitePWAOptions } from 'vite-plugin-pwa'

const pwaOptions: Partial<VitePWAOptions> = {
    // outDir: 'dist/static',
    manifest: {
        name: 'Quicktrack',
        short_name: 'Quicktrack',
        theme_color: '#3f88c5',
        icons: [
            {
                src: 'icons/manifest-icon-192.png',
                sizes: '192x192',
                type: 'image/png',
                purpose: 'maskable any',
            },
            {
                src: 'icons/manifest-icon-512.png',
                sizes: '512x512',
                type: 'image/png',
                purpose: 'maskable any',
            },
        ],
        start_url: '/',
        display: 'standalone',
        background_color: '#131516',
    },
    // iconPaths: {
    //     favicon32: 'static/icons/favicon-32x32.png',
    //     favicon16: null,
    //     appleTouchIcon: 'static/icons/apple-touch-icon-152x152.png',
    //     // maskIcon: 'static/icons/safari-pinned-tab.svg',
    //     // msTileImage: 'static/icons/msapplication-icon-144x144.png',
    // },
    // manifestPath: 'static/manifest.json',
    // workboxPluginMode: 'GenerateSW',
    // workboxOptions: {
    //     // navigateFallback: '/index.html',
    //     precacheManifestFilename:
    //         './static/js/precache-manifest.[manifestHash].js',
    // },
}

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue(), VitePWA(pwaOptions)],
    build: {
        assetsDir: 'static',
    },
    server: {
        proxy: {
            '/api': 'http://localhost:5000',
            '/accounts/me': 'http://localhost:5000',
            '/accounts/login': 'http://localhost:5000',
        },
    },
})
