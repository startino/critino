import * as schemes from '$lib/theme/schemes';

type Mode =
	| 'light'
	| 'lightMediumContrast'
	| 'lightHighContrast'
	| 'dark'
	| 'darkMediumContrast'
	| 'darkHighContrast';

export const system = (): Mode => {
	if (typeof window === 'undefined') return 'light';

	const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
	prefersDarkScheme.addEventListener('change', (event) => {
		if (event.matches) {
			console.log('User prefers dark mode');
			setMode('dark');
		} else {
			console.log('User prefers light mode');
			setMode('light');
		}
	});
	return prefersDarkScheme.matches ? 'dark' : 'light'; // returns a boolean indicating the current color scheme
};

export const resetMode = () => {
	setMode(system());
};

export const setMode = (mode: Mode) => {
	localStorage.setItem('theme', mode);

	if (typeof window !== 'undefined') {
		for (const css of schemes[getMode()]) {
			document.documentElement.style.setProperty(
				css.split(': ')[0],
				css.split(': ')[1].replace(';', '')
			);
		}
	}
};

export const getMode = (): Mode => {
	try {
		return (localStorage.getItem('theme') as Mode) || system();
	} catch (e) {
		return system();
	}
};
