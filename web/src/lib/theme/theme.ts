export type MD3Scheme = {
	primary: string;
	surfaceTint: string;
	onPrimary: string;
	primaryContainer: string;
	onPrimaryContainer: string;
	secondary: string;
	onSecondary: string;
	secondaryContainer: string;
	onSecondaryContainer: string;
	tertiary: string;
	onTertiary: string;
	tertiaryContainer: string;
	onTertiaryContainer: string;
	error: string;
	onError: string;
	errorContainer: string;
	onErrorContainer: string;
	background: string;
	onBackground: string;
	surface: string;
	onSurface: string;
	surfaceVariant: string;
	onSurfaceVariant: string;
	outline: string;
	outlineVariant: string;
	shadow: string;
	scrim: string;
	inverseSurface: string;
	inverseOnSurface: string;
	inversePrimary: string;
	primaryFixed: string;
	onPrimaryFixed: string;
	primaryFixedDim: string;
	onPrimaryFixedVariant: string;
	secondaryFixed: string;
	onSecondaryFixed: string;
	secondaryFixedDim: string;
	onSecondaryFixedVariant: string;
	tertiaryFixed: string;
	onTertiaryFixed: string;
	tertiaryFixedDim: string;
	onTertiaryFixedVariant: string;
	surfaceDim: string;
	surfaceBright: string;
	surfaceContainerLowest: string;
	surfaceContainerLow: string;
	surfaceContainer: string;
	surfaceContainerHigh: string;
	surfaceContainerHighest: string;
};

const getRGBColor = (hex: string, key: string) => {
	let color = hex.replace(/#/g, '');
	// rgb values
	var r = parseInt(color.substring(0, 2), 16);
	var g = parseInt(color.substring(2, 4), 16);
	var b = parseInt(color.substring(4, 6), 16);

	return `--color-${key}: ${r}, ${g}, ${b};`;
};

export const generateTheme = (md3Scheme: MD3Scheme) => {
	const theme = {
		primary: md3Scheme.primary,
		'primary-on': md3Scheme.onPrimary,
		'primary-container': md3Scheme.primaryContainer,
		'primary-container-on': md3Scheme.onPrimaryContainer,
		'primary-inverse': md3Scheme.inversePrimary,
		'primary-foreground': md3Scheme.onPrimary,
		secondary: md3Scheme.secondary,
		'secondary-on': md3Scheme.onSecondary,
		'secondary-container': md3Scheme.secondaryContainer,
		'secondary-container-on': md3Scheme.onSecondaryContainer,
		tertiary: md3Scheme.tertiary,
		'tertiary-on': md3Scheme.onTertiary,
		'tertiary-container': md3Scheme.tertiaryContainer,
		'tertiary-container-on': md3Scheme.onTertiaryContainer,
		surface: md3Scheme.surface,
		'surface-on': md3Scheme.onSurface,
		'surface-variant': md3Scheme.surfaceVariant,
		'surface-variant-on': md3Scheme.onSurfaceVariant,
		background: md3Scheme.background,
		'background-on': md3Scheme.onBackground,
		outline: md3Scheme.outline,
		'outline-variant': md3Scheme.outlineVariant,
		error: md3Scheme.error,
		'error-on': md3Scheme.onError,
		'error-container': md3Scheme.errorContainer,
		'error-container-on': md3Scheme.onErrorContainer,
		success: md3Scheme.secondary,
		'success-on': md3Scheme.onSecondary,
		'success-container': md3Scheme.secondaryContainer,
		'success-container-on': md3Scheme.onSecondaryContainer,
	};

	const themeList = Object.entries(theme).map(([key, value]) => getRGBColor(value, key));

	return themeList;
};
