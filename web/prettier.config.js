/**
 * @see https://prettier.io/docs/en/configuration.html
 * @type {import("prettier").Config}
 */
const config = {
	plugins: ['prettier-plugin-svelte', 'prettier-plugin-tailwindcss'],
	overrides: [{ files: '*.svelte', options: { parser: 'svelte' } }],
	semi: true,
	tabWidth: 4,
	useTabs: true,
	printWidth: 100,
	singleQuote: true,
	trailingComma: 'es5',
	htmlWhitespaceSensitivity: 'ignore',
	svelteSortOrder: 'options-styles-scripts-markup',
};

export default config;
