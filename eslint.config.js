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
    // Ignore paths that should not be linted
    ignores: [
      'greenova/media/**/*', // Uploaded media files
      'greenova/staticfiles/**/*', // Collected static files
      'greenova/logs/**/*', // Log files
      'node_modules/**/*', // Node.js dependencies
      '.venv/**', // Python virtual environment
      '.vscode/**/*', // VS Code settings
      'dist/**/*', // Distribution files
      'vendor/**', // Vendor libraries
    ],
  },
  ...compat.extends('eslint:recommended', 'plugin:prettier/recommended'),
  {
    languageOptions: {
      globals: {
        ...globals.browser, // Browser global variables
        ...globals.node, // Node.js global variables
      },
      ecmaVersion: 2024, // Use ECMAScript 2024 features
      sourceType: 'module', // Use ES modules
    },
    rules: {
      indent: ['error', 2], // Enforce 2-space indentation
      'linebreak-style': ['error', 'unix'], // Enforce Unix-style line endings
      quotes: ['error', 'single', { avoidEscape: true }], // Enforce single quotes
      semi: ['error', 'always'], // Enforce semicolons
      'no-unused-vars': 'warn', // Warn about unused variables
      'no-console': 'warn', // Warn about console statements
      'prettier/prettier': ['error', { singleQuote: true }], // Enforce Prettier rules
    },
  },
];

// Added comments to explain the purpose of specific rules and ignored paths.
