/**
 * Greenova Tailwind Configuration
 *
 * This configuration is designed to complement PicoCSS, not replace it.
 * We map Tailwind's color system to use Greenova design tokens and
 * ensure the two systems work together without conflicts.
 */

module.exports = {
  // Only process files that specifically use Tailwind
  content: [
    './greenova/templates/**/*.html',
    './greenova/static/js/**/*.js',
    './greenova/*/templates/**/*.html',
  ],

  // Important: This ensures Tailwind doesn't override PicoCSS
  important: false,

  // Disable core plugins that PicoCSS already handles well
  corePlugins: {
    preflight: false, // PicoCSS handles normalization
    container: false, // PicoCSS handles containers
  },

  theme: {
    // Extend default theme with Greenova design tokens
    extend: {
      // Map Tailwind colors to Greenova color variables
      colors: {
        green: {
          primary: 'var(--greenova-green-primary)',
          secondary: 'var(--greenova-green-secondary)',
          tertiary: 'var(--greenova-green-tertiary)',
        },
        beige: {
          primary: 'var(--greenova-beige-primary)',
          secondary: 'var(--greenova-beige-secondary)',
        },
        bg: {
          primary: 'var(--greenova-background-primary)',
          secondary: 'var(--greenova-background-secondary)',
        },
        text: {
          'primary-dark': 'var(--greenova-text-primary-dark)',
          'secondary-dark': 'var(--greenova-text-secondary-dark)',
          'tertiary-dark': 'var(--greenova-text-tertiary-dark)',
          'primary-light': 'var(--greenova-text-primary-light)',
        },
        notif: {
          high: 'var(--greenova-notif-primary-high)',
          mid: 'var(--greenova-notif-primary-mid)',
          low: 'var(--greenova-notif-primary-low)',
        },
      },

      // Match spacing to Greenova design system
      spacing: {
        small: 'var(--greenova-spacing-small)',
        base: 'var(--greenova-spacing)',
        large: 'var(--greenova-spacing-large)',
        'padding-small': 'var(--greenova-padding-small)',
        padding: 'var(--greenova-padding)',
        'padding-large': 'var(--greenova-padding-large)',
      },

      // Match border radius to Greenova design system
      borderRadius: {
        DEFAULT: 'var(--greenova-border-radius)',
        small: 'var(--greenova-border-radius-small)',
        chat: 'var(--greenova-chat-border-radius)',
        'chat-user': 'var(--greenova-chat-user-border-radius)',
        'chat-bot': 'var(--greenova-chat-bot-border-radius)',
      },

      // Match typography to Greenova design system
      fontSize: {
        title: 'var(--greenova-title-size)',
        subtitle: 'var(--greenova-subtitle-size)',
        text: 'var(--greenova-text-size)',
        'input-label': 'var(--greenova-input-label)',
        input: 'var(--greenova-input-size)',
        table: 'var(--greenova-table-size)',
        button: 'var(--greenova-button-size)',
      },

      // Add Greenova font family
      fontFamily: {
        greenova: 'var(--greenova-font-family)',
      },

      // Custom shadow matching Greenova design
      boxShadow: {
        greenova: 'var(--greenova-shadow)',
      },
    },
  },

  // Define custom plugins for Greenova-specific needs
  plugins: [
    // Plugin to generate WCAG-compliant focus styles
    function ({ addUtilities }) {
      const accessibilityUtilities = {
        '.focus-accessible': {
          outline: '3px solid var(--greenova-green-primary)',
          'outline-offset': '2px',
        },
      };
      addUtilities(accessibilityUtilities);
    },

    // Plugin for responsive data visualization
    function ({ addComponents }) {
      const chartComponents = {
        '.responsive-chart': {
          width: '100%',
          height: 'auto',
          'min-height': '300px',
        },
      };
      addComponents(chartComponents, { respectImportant: true });
    },
  ],
};
