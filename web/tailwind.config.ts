import colorConfig from './theme/color';
import typographyConfig from './theme/typography';

/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: colorConfig,
			typography: () => ({
				...typographyConfig(),
				...{
					DEFAULT: {},
				},
			}),
		},
	},

	plugins: [
		require('@tailwindcss/forms'),
		require('@tailwindcss/typography'),
		require('@tailwindcss/aspect-ratio'),
	],
};
