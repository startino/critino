import c from './md3';

const scheme = c.schemes.dark;

const colors = {
	// Primary tones
	primary: {
		DEFAULT: scheme.primary,
		on: {
			DEFAULT: scheme.onPrimary,
		},
		container: {
			DEFAULT: scheme.primaryContainer,
			on: {
				DEFAULT: scheme.onPrimaryContainer,
			},
		},
		inverse: {
			DEFAULT: scheme.inversePrimary,
		},
	},

	// Secondary tones
	secondary: {
		DEFAULT: scheme.secondary,
		on: {
			DEFAULT: scheme.onSecondary,
		},
		container: {
			DEFAULT: scheme.secondaryContainer,
			on: {
				DEFAULT: scheme.onSecondaryContainer,
			},
		},
	},

	// Tertiary tones
	tertiary: {
		DEFAULT: scheme.tertiary,
		on: {
			DEFAULT: scheme.onTertiary,
		},
		container: {
			DEFAULT: scheme.tertiaryContainer,
			on: {
				DEFAULT: scheme.onTertiaryContainer,
			},
		},
	},

	// Neutral tones (md3 names them as 'surface')
	surface: {
		DEFAULT: scheme.surface,
		on: {
			DEFAULT: scheme.onSurface,
			inverse: {
				DEFAULT: scheme.inverseOnSurface,
			},
		},
		// Neutral variant tones
		variant: {
			DEFAULT: scheme.surfaceVariant,
			on: {
				DEFAULT: scheme.onSurfaceVariant,
			},
		},
	},

	// Background tones
	background: {
		DEFAULT: scheme.background,
		on: {
			DEFAULT: scheme.onBackground,
		},
	},

	outline: {
		DEFAULT: scheme.outline,
		variant: {
			DEFAULT: scheme.outlineVariant,
		},
	},

	// Error tones
	error: {
		DEFAULT: scheme.error,
		on: {
			DEFAULT: scheme.onError,
		},
		container: {
			DEFAULT: scheme.errorContainer,
			on: {
				DEFAULT: scheme.onErrorContainer,
			},
		},
	},

	// Success tones (md3 didn't produce the extended color but secondary color is close)
	success: {
		DEFAULT: scheme.secondary,
		on: {
			DEFAULT: scheme.onSecondary,
		},
		container: {
			DEFAULT: scheme.secondaryContainer,
			on: {
				DEFAULT: scheme.onSecondaryContainer,
			},
		},
	},
};

// automated key assignments
colors.foreground = colors.background.on.DEFAULT;
colors.primary.foreground = colors.primary.on.DEFAULT;
colors.secondary.foreground = colors.secondary.on.DEFAULT;
colors.tertiary.foreground = colors.tertiary.on.DEFAULT;
colors.surface.foreground = colors.surface.on.DEFAULT;
colors.surface.variant.foreground = colors.surface.on.DEFAULT;
colors.background.foreground = colors.background.on.DEFAULT;
colors.outline.foreground = colors.outline.DEFAULT;
colors.error.foreground = colors.error.on.DEFAULT;
colors.success.foreground = colors.success.on.DEFAULT;

colors.accent = colors.tertiary.DEFAULT;
colors.border = colors.primary.DEFAULT;
colors.input = colors.primary.DEFAULT;
colors.ring = colors.primary.DEFAULT;

colors.destructive = {
	DEFAULT: colors.error.DEFAULT,
	foreground: colors.error.on.DEFAULT,
};
colors.muted = {
	DEFAULT: colors.surface.variant.DEFAULT,
	foreground: colors.surface.variant.on.DEFrULT,
};

colors.popover = {
	DEFAULT: colors.surface.DEFAULT,
	foreground: colors.surface.on.DEFAULT,
};
colors.card = {
	DEFAULT: colors.primary.DEFAULT,
	foreground: colors.surface.on.DEFAULT,
};

export default colors;
