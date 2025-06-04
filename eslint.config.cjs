const js = require('@eslint/js')
const tsPlugin = require('@typescript-eslint/eslint-plugin')
const tsParser = require('@typescript-eslint/parser')

module.exports = [
  js.configs.recommended,
  {
    files: ['**/*.{js,jsx,ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      parser: tsParser,
      parserOptions: {
        ecmaFeatures: {
          jsx: true
        }
      }
    },
    plugins: {
      '@typescript-eslint': tsPlugin
    },
    rules: {
      // JavaScript/TypeScript rules
      'no-unused-vars': 'off', // Turn off base rule to use TypeScript version
      '@typescript-eslint/no-unused-vars': 'error',
      'no-console': 'error',
      'max-len': ['error', { code: 80 }],

      // TypeScript-specific rules (manually defined instead of using extends)
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/no-inferrable-types': 'error',
      '@typescript-eslint/prefer-as-const': 'error',
      '@typescript-eslint/no-array-constructor': 'error',
      '@typescript-eslint/no-empty-function': 'error',
      '@typescript-eslint/no-extra-non-null-assertion': 'error',
      '@typescript-eslint/no-misused-new': 'error',
      '@typescript-eslint/no-namespace': 'error',
      '@typescript-eslint/no-non-null-asserted-optional-chain': 'error',
      '@typescript-eslint/no-this-alias': 'error',
      '@typescript-eslint/no-unnecessary-type-constraint': 'error',
      '@typescript-eslint/no-unsafe-declaration-merging': 'error',
      '@typescript-eslint/prefer-namespace-keyword': 'error',
      '@typescript-eslint/triple-slash-reference': 'error'
    }
  },
  {
    files: ['**/*.ts', '**/*.tsx'],
    rules: {
      // Additional TypeScript-only rules
      '@typescript-eslint/adjacent-overload-signatures': 'error',
      '@typescript-eslint/ban-ts-comment': 'error',
      '@typescript-eslint/no-duplicate-enum-values': 'error',
      '@typescript-eslint/no-loss-of-precision': 'error',
      '@typescript-eslint/no-non-null-asserted-nullish-coalescing': 'error',
      '@typescript-eslint/no-var-requires': 'error'
    }
  }
]
