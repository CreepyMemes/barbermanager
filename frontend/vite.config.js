import { defineConfig } from 'vite';
import * as path from 'path';
import react from '@vitejs/plugin-react';
import eslint from 'vite-plugin-eslint';

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    eslint({
      failOnError: true, // Stop build on ESLint errors
      failOnWarning: false, // Don't stop build on warnings
    }),
  ],

  resolve: {
    alias: [
      { find: '@assets', replacement: path.resolve(__dirname, './src/assets') },
      { find: '@styles', replacement: path.resolve(__dirname, './src/styles') },
      { find: '@hooks', replacement: path.resolve(__dirname, './src/hooks') },
      { find: '@contexts', replacement: path.resolve(__dirname, './src/contexts') },
      { find: '@components', replacement: path.resolve(__dirname, './src/components') },
      { find: '@pages', replacement: path.resolve(__dirname, './src/pages') },
      { find: '@routes', replacement: path.resolve(__dirname, './src/routes') },
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
  },
});
