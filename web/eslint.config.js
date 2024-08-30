import tsParser from '@typescript-eslint/parser';
import svelteConfig from './svelte.config.js';
import svelteParser from 'svelte-eslint-parser';

export default [
	{
		languageOptions: {
			parser: tsParser,
			parserOptions: {
				extraFileExtensions: ['.svelte'], // This is a required setting in `@typescript-eslint/parser` v4.24.0.
				svelteConfig,
			},
		},
	},
	{
		files: ['**/*.svelte', '*.svelte'],
		languageOptions: {
			parser: svelteParser,
			// Parse the `<script>` in `.svelte` as TypeScript by adding the following configuration.
			parserOptions: {
				parser: tsParser,
				svelteConfig,
			},
		},
	},
];
