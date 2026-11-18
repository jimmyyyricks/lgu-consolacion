// https://nuxt.com/docs/api/configuration/nuxt-config
import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({

  modules: ['@nuxt/eslint', '@nuxt/ui', '@vueuse/nuxt', '@pinia/nuxt', '@nuxt/image', '@nuxt/fonts'],

  ssr: true,

  devtools: {
    enabled: process.env.NODE_ENV !== 'production'
  },

  css: [
    '~/assets/css/main.css'
  ],

  colorMode: {
    preference: 'light',
    fallback: 'light'
  },

  runtimeConfig: {
    public: {
      apiUrl: process.env.NUXT_PUBLIC_API_URL || '/api'
    }
  },

  routeRules: {
    '/admin': { ssr: false },
    '/admin/**': { ssr: false }
  },
  experimental: {
    appManifest: false
  },

  compatibilityDate: '2025-01-15',

  vite: {
    build: {
      chunkSizeWarningLimit: 1000,
      rollupOptions: {
        output: {
          manualChunks: {
            pinia: ['pinia'],
            vue: ['vue', 'vue-router'],
            utils: ['@vueuse/core', 'scule']
          }
        }
      }
    }
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  },

  icon: {
    collections: ['lucide', 'simple-icons']
  }
})
