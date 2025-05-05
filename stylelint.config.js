export default {
  extends: [
    'stylelint-config-standard',
    'stylelint-config-recommended',
    'stylelint-config-tailwindcss',
  ],
  rules: {
    // General rules
    // Removing max-line-length rule as it's not supported in Stylelint v16
    // Line lengths are handled by Prettier's printWidth setting instead
    'no-descending-specificity': null, // Allow for component-based CSS organization
    'import-notation': null, // Allow CSS imports as used throughout the project

    // Selector patterns
    'selector-class-pattern': null, // Allow BEM and other naming patterns
    'selector-nested-pattern': null, // Allow various nesting patterns including &:hover
    'selector-id-pattern': null, // Allow flexibility for existing IDs

    // CSS features
    'at-rule-no-unknown': [
      true,
      {
        ignoreAtRules: [
          // Tailwind directives
          'tailwind',
          'apply',
          'layer',
          'variants',
          'responsive',
          'screen',
          // PostCSS features
          'import',
          'nest',
          'custom-media',
          'custom-selector',
          // Additional features
          'value',
          'property',
          'container-type',
          'media',
          'supports',
        ],
      },
    ],

    // Custom properties
    'custom-property-pattern': [
      '^([a-z][a-z0-9]*)(-[a-z0-9]+)*$',
      {
        message: 'Expected custom property name to be kebab-case',
      },
    ],

    // Comments and documentation
    'comment-empty-line-before': null, // Allow flexible comment placement
    'comment-whitespace-inside': null, // Allow comment formatting flexibility

    // Values and properties
    'value-keyword-case': [
      'lower',
      {
        ignoreProperties: ['/^--/'],
        camelCaseSvgKeywords: true,
      },
    ],
    'property-no-vendor-prefix': null, // Allow vendor prefixes for compatibility
    'value-no-vendor-prefix': null, // Allow vendor prefixes for compatibility

    // Color handling
    'color-function-notation': 'modern', // Prefer modern color function notation
    'color-no-hex': null, // Allow hex colors

    // Media queries
    'media-feature-range-notation': 'prefix', // Allow both prefix and context notation

    // Accessibility
    'declaration-property-value-no-unknown': true, // Catch typos in property values
    'font-family-name-quotes': 'always-where-recommended', // Follow best practices for font names
    'font-family-no-duplicate-names': true, // Prevent duplicate font names
  },
  ignoreFiles: [
    // Don't process vendor files or generated files
    'greenova/static/css/vendor/**',
    'greenova/theme/static/css/dist/**',
    'node_modules/**',
    '**/*.html',
    '**/*.jinja',
  ],
};
