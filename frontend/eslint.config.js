import js from '@eslint/js';
import globals from 'globals';

import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';

import prettier from 'eslint-plugin-prettier/recommended';

export default [
  {
    ignores: ['dist/*'],
  },

  {
    files: ['**/*.{js,mjs,cjs,jsx}'],

    languageOptions: {
      ecmaVersion: 2020,
      globals: {
        ...globals.browser,
        __dirname: true,
      },

      parserOptions: {
        sourceType: 'module',
        ecmaVersion: 'latest',
        ecmaFeatures: { jsx: true },
      },
    },

    settings: { react: { version: '18.3' } },

    // Used plugins
    plugins: {
      react,
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },

    // ESLint rules configuration
    rules: {
      ...js.configs.recommended.rules,
      ...react.configs.recommended.rules,
      ...react.configs['jsx-runtime'].rules,
      ...reactHooks.configs.recommended.rules,
      'react/jsx-no-target-blank': 'off',
      'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],

      'no-unused-vars': ['warn', { argsIgnorePattern: '^_$', varsIgnorePattern: '^_$' }],
      'react/prop-types': 'off',
    },
  },

  prettier,
];
