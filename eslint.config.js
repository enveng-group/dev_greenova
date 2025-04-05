import globals from 'globals';
import js from '@eslint/js';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { FlatCompat } from '@eslint/eslintrc';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all,
});

export default [
  {
    ignores: [
      'greenova/static/**/*',
      'greenova/media/**/*',
      'greenova/staticfiles/**/*',
      'greenova/logs/**/*',
      'node_modules/**/*',
      '.venv/**',
      '.vscode/**/*',
      'dist/**/*',
      'vendor/**',
    ],
  },
  ...compat.extends('eslint:recommended', 'plugin:prettier/recommended'),
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
      },
      ecmaVersion: 2024,
      sourceType: 'module',
    },
    rules: {
      indent: ['error', 2],
      'linebreak-style': ['error', 'unix'],
      quotes: ['error', 'single', { avoidEscape: true }],
      semi: ['error', 'always'],
      'no-unused-vars': 'warn',
      'no-console': 'warn',
      'prettier/prettier': ['error', { singleQuote: true }],
    },
  },
];
