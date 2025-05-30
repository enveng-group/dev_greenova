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
		"./greenova/templates/**/*.html",
		"./greenova/static/js/**/*.js",
		"./greenova/*/templates/**/*.html",
	],

	// Important: This ensures Tailwind doesn't override PicoCSS
	important: false,

	// Disable core plugins that PicoCSS already handles well
	corePlugins: {
		preflight: false, // PicoCSS handles normalization
		container: false, // PicoCSS handles containers

		// Additional core plugins to disable to avoid conflicts
		fontSize: false, // Use PicoCSS typography
		fontFamily: false, // Use PicoCSS fonts
	},

	// Enable experimental features for modern CSS
	future: {
		hoverOnlyWhenSupported: true,
		respectDefaultRingColorOpacity: true,
		disableColorOpacityUtilitiesByDefault: true,
		relativeContentPathsByDefault: true,
	},

	theme: {
		// Extend default theme with Greenova design tokens
		extend: {
			// Map Tailwind colors to Greenova color variables
			colors: {
				green: {
					primary: "var(--greenova-green-primary)",
					secondary: "var(--greenova-green-secondary)",
					tertiary: "var(--greenova-green-tertiary)",
				},
				beige: {
					primary: "var(--greenova-beige-primary)",
					secondary: "var(--greenova-beige-secondary)",
				},
				bg: {
					primary: "var(--greenova-background-primary)",
					secondary: "var(--greenova-background-secondary)",
				},
				text: {
					"primary-dark": "var(--greenova-text-primary-dark)",
					"secondary-dark": "var(--greenova-text-secondary-dark)",
					"tertiary-dark": "var(--greenova-text-tertiary-dark)",
					"primary-light": "var(--greenova-text-primary-light)",
				},
				notif: {
					high: "var(--greenova-notif-primary-high)",
					mid: "var(--greenova-notif-primary-mid)",
					low: "var(--greenova-notif-primary-low)",
				},
			},

			// Enhanced spacing system with CSS logical properties
			spacing: {
				small: "var(--greenova-spacing-small)",
				base: "var(--greenova-spacing)",
				large: "var(--greenova-spacing-large)",
				"padding-small": "var(--greenova-padding-small)",
				padding: "var(--greenova-padding)",
				"padding-large": "var(--greenova-padding-large)",

				// Logical properties for RTL support
				"inline-start": "var(--greenova-spacing-inline-start)",
				"inline-end": "var(--greenova-spacing-inline-end)",
				"block-start": "var(--greenova-spacing-block-start)",
				"block-end": "var(--greenova-spacing-block-end)",
			},

			// Match border radius to Greenova design system
			borderRadius: {
				DEFAULT: "var(--greenova-border-radius)",
				small: "var(--greenova-border-radius-small)",
				chat: "var(--greenova-chat-border-radius)",
				"chat-user": "var(--greenova-chat-user-border-radius)",
				"chat-bot": "var(--greenova-chat-bot-border-radius)",
			},

			// Match typography to Greenova design system
			// Only extend what PicoCSS doesn't cover
			fontSize: {
				"input-label": "var(--greenova-input-label)",
				input: "var(--greenova-input-size)",
				table: "var(--greenova-table-size)",
				button: "var(--greenova-button-size)",
			},

			// Add Greenova font family
			fontFamily: {
				greenova: "var(--greenova-font-family)",
			},

			// Custom shadow matching Greenova design
			boxShadow: {
				greenova: "var(--greenova-shadow)",
			},

			// Enhanced container queries support
			containers: {
				xs: "20rem",
				sm: "24rem",
				md: "28rem",
				lg: "32rem",
				xl: "36rem",
				"2xl": "42rem",
				"3xl": "48rem",
			},

			// Screen reader and accessibility utilities
			aria: {
				invalid: 'invalid="true"',
				disabled: 'disabled="true"',
				checked: 'checked="true"',
				expanded: 'expanded="true"',
				hidden: 'hidden="true"',
			},

			// Motion-safe animations
			animation: {
				"safe-spin": "spin 1s linear infinite",
				"safe-ping": "ping 1s cubic-bezier(0, 0, 0.2, 1) infinite",
				"safe-pulse": "pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
			},
		},
	},

	plugins: [
		// Official Tailwind plugins
		require("@tailwindcss/typography")({
			className: "tw-prose", // Prefix typography classes to avoid conflicts
		}),
		require("@tailwindcss/forms")({
			strategy: "class", // Only generate classes when explicitly used
		}),
		require("@tailwindcss/aspect-ratio"),
		require("@tailwindcss/container-queries"),

		// Additional plugins for enhanced features
		require("tailwindcss-animate"),
		require("tailwindcss-logical"),
		require("tailwindcss-fluid-type"),
		require("tailwindcss-opentype"),
		require("tailwind-scrollbar-hide"),

		// Plugin to generate WCAG-compliant focus styles
		({ addUtilities }) => {
			const accessibilityUtilities = {
				".focus-accessible": {
					outline: "3px solid var(--greenova-green-primary)",
					"outline-offset": "2px",
				},
			};
			addUtilities(accessibilityUtilities);
		},

		// Enhanced chart components
		({ addComponents }) => {
			const chartComponents = {
				".responsive-chart": {
					width: "100%",
					height: "auto",
					"min-height": "300px",
					"@container (min-width: 640px)": {
						"min-height": "400px",
					},
				},
			};
			addComponents(chartComponents, { respectImportant: true });
		},

		// Add motion-safe utilities
		({ addUtilities }) => {
			addUtilities({
				".motion-safe": {
					"@media (prefers-reduced-motion: no-preference)": {
						"transition-property": "all",
						"transition-timing-function": "cubic-bezier(0.4, 0, 0.2, 1)",
						"transition-duration": "150ms",
					},
				},
				".motion-reduce": {
					"@media (prefers-reduced-motion: reduce)": {
						"transition-property": "none",
						animation: "none",
					},
				},
			});
		},

		// Add print utilities
		({ addUtilities }) => {
			addUtilities({
				".print-only": {
					"@media screen": {
						display: "none",
					},
				},
				".no-print": {
					"@media print": {
						display: "none",
					},
				},
			});
		},
	],

	// Layer configuration for proper cascade
	layers: {
		base: "base",
		components: "components",
		utilities: "utilities",
		"greenova-custom": "greenova-custom",
	},
};
