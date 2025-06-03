export default [
	{
		files: ["**/*.{js,jsx,ts,tsx}"],
		languageOptions: {
			ecmaVersion: 2022,
			sourceType: "module",
		},
		plugins: {
			prettier: require("eslint-plugin-prettier"),
		},
		extends: [
			"eslint:recommended",
			"plugin:@typescript-eslint/recommended",
			"plugin:prettier/recommended",
		],
		rules: {
			"prettier/prettier": "error",
			"no-unused-vars": "error",
			"no-console": "error",
			"max-len": ["error", { code: 80 }],
		},
	},
];
