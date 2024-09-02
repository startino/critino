import c from './md3';
import { generateTheme } from './theme';

const scheme = c.schemes;

const light = generateTheme(scheme.light);
const lightMediumContrast = generateTheme(scheme['light-medium-contrast']);
const lightHighContrast = generateTheme(scheme['light-high-contrast']);

const dark = generateTheme(scheme.dark);
const darkMediumContrast = generateTheme(scheme['dark-medium-contrast']);
const darkHighContrast = generateTheme(scheme['dark-high-contrast']);

export {
	light,
	lightMediumContrast,
	lightHighContrast,
	dark,
	darkMediumContrast,
	darkHighContrast,
};
