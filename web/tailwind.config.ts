import colorsConfig from './theme/colors';
import typographyConfig from './theme/typography';

/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: colorsConfig,
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
