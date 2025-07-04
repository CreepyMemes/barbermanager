import { defineConfig } from 'vite';
import { Buffer } from 'buffer';
import * as path from 'path';
import react from '@vitejs/plugin-react';
import eslint from 'vite-plugin-eslint';
import svgr from 'vite-plugin-svgr';

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    svgr({
      exportAsDefault: true, // default export is a React component
      include: '**/*.svg?react', // handle the ?react suffix
    }),
    eslint({
      failOnError: true, // Stop build on ESLint errors
      failOnWarning: false, // Don't stop build on warnings
    }),
  ],

  resolve: {
    alias: [
      { find: '@assets', replacement: path.resolve(__dirname, './assets') },
      { find: '@api', replacement: path.resolve(__dirname, './src/api') },
      { find: '@components', replacement: path.resolve(__dirname, './src/components') },
      { find: '@contexts', replacement: path.resolve(__dirname, './src/contexts') },
      { find: '@hooks', replacement: path.resolve(__dirname, './src/hooks') },
      { find: '@pages', replacement: path.resolve(__dirname, './src/pages') },
      { find: '@providers', replacement: path.resolve(__dirname, './src/providers') },
      { find: '@routes', replacement: path.resolve(__dirname, './src/routes') },
      { find: '@styles', replacement: path.resolve(__dirname, './src/styles') },
      { find: '@utils', replacement: path.resolve(__dirname, './src/utils') },
    ],
  },

  css: {
    modules: {
      localsConvention: 'camelCaseOnly',
    },
  },

  server: {
    host: true,
    watch: {
      usePolling: true, // For hot reloading
    },
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false,
        ws: true, // websocket
        configure: (proxy, _options) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            let bodyData = [];
            req.on('data', (chunk) => {
              bodyData.push(chunk);
            });
            req.on('end', () => {
              if (bodyData.length > 0) {
                const raw = Buffer.concat(bodyData).toString();
                console.log(`[proxyReq] ${req.method} ${req.url} -- Request Body:`, raw);
              }
            });
          });

          proxy.on('proxyRes', (proxyRes, req, res) => {
            let body = [];
            proxyRes.on('data', (chunk) => {
              body.push(chunk);
            });
            proxyRes.on('end', () => {
              if (body.length > 0) {
                const raw = Buffer.concat(body).toString();
                console.log(`[proxyRes] ${req.method} ${req.url} -- Response Body:`, raw);
              }
            });
          });
        },
      },
      '/media': {
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false,
        ws: false,
      },
    },
  },
});
