import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { mdsvex } from 'mdsvex';
import prettierPlugin from 'prettier-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	extensions: ['.svelte', '.md'],
	// Consult https://kit.svelte.dev/docs/integrations#preprocessors
	// for more information about preprocessors
	preprocess: [
		vitePreprocess(),
		mdsvex({
			extensions: ['.md'],
		}),
	],

	kit: {
		// adapter-auto only supports some environments, see https://kit.svelte.dev/docs/adapter-auto for a list.
		// If your environment is not supported or you settled on a specific environment, switch out the adapter.
		// See https://kit.svelte.dev/docs/adapters for more information about adapters.
		adapter: adapter({
			maxDuration: 300, // Set the timeout to 300 seconds
			headers: [
				{
					source: '/(.*)',
					headers: [
						{
							key: 'Access-Control-Allow-Origin',
							value: '*',
						},
						{
							key: 'Access-Control-Allow-Credentials',
							value: 'true',
						},
						{
							key: 'Access-Control-Allow-Methods',
							value: '*',
						},
						{
							key: 'Access-Control-Allow-Headers',
							value: '*',
						},
					],
				},
			],
		}),
		alias: {
			$styling: './src/app.pcss',
		},
		csrf: {
			checkOrigin: false,
		},
	},

	prettier: {
		plugin: prettierPlugin,
		options: {
			overrides: [{ files: '*.svelte', options: { parser: 'svelte' } }],
			semi: true,
			tabWidth: 4,
			useTabs: true,
			printWidth: 100,
			singleQuote: true,
			trailingComma: 'es5',
			htmlWhitespaceSensitivity: 'ignore',
			svelteSortOrder: 'options-styles-scripts-markup',
		},
	},
};

export default config;
