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
      failOnWarning: false, // (Optional) Stop build on warnings
    }),
  ],
  resolve: {
    alias: [
      { find: '@app', replacement: path.resolve(__dirname, './src/app') },
      { find: '@components', replacement: path.resolve(__dirname, './src/components') },
      { find: '@common', replacement: path.resolve(__dirname, './src/common') },
      { find: '@assets', replacement: path.resolve(__dirname, './src/assets') },
      { find: '@data', replacement: path.resolve(__dirname, './src/data') },
    ],
  },
  css: {
    modules: {
      localsConvention: 'camelCaseOnly',
    },
  },

  //In Django, prefix your routes with /api/ (e.g., path('api/hello/', ...)) to keep backend endpoints well-scoped.
  server: {
    host: true,
    watch: {
      usePolling: true,
    },
  },
});
