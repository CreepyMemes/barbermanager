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
      { find: '@app', replacement: path.resolve(__dirname, './src/app') },
      { find: '@components', replacement: path.resolve(__dirname, './src/components') },
      { find: '@assets', replacement: path.resolve(__dirname, './src/assets') },
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
