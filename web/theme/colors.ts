const withOpacity = (key: string) => {
	return ({ opacityValue }) => {
		if (opacityValue !== undefined) {
			return `rgba(var(${key}), ${opacityValue})`;
		}
		return `rgb(var(${key}))`;
	};
};

const colors = {
	// Primary tones
	primary: {
		DEFAULT: withOpacity('--color-primary'),
		on: {
			DEFAULT: withOpacity('--color-primary-on'),
		},
		container: {
			DEFAULT: withOpacity('--color-primary-container'),
			on: {
				DEFAULT: withOpacity('--color-primary-container-on'),
			},
		},
		inverse: {
			DEFAULT: withOpacity('--color-primary-inverse'),
		},
		foreground: withOpacity('--color-primary-on'),
	},

	// Secondary tones
	secondary: {
		DEFAULT: withOpacity('--color-secondary'),
		on: {
			DEFAULT: withOpacity('--color-secondary-on'),
		},
		container: {
			DEFAULT: withOpacity('--color-secondary-container'),
			on: {
				DEFAULT: withOpacity('--color-secondary-container-on'),
			},
		},
		foreground: withOpacity('--color-secondary-on'),
	},

	// Tertiary tones
	tertiary: {
		DEFAULT: withOpacity('--color-tertiary'),
		on: {
			DEFAULT: withOpacity('--color-tertiary-on'),
		},
		container: {
			DEFAULT: withOpacity('--color-tertiary-container'),
			on: {
				DEFAULT: withOpacity('--color-tertiary-container-on'),
			},
		},
		foreground: withOpacity('--color-tertiary-on'),
	},

	// Neutral tones (md3 names them as 'surface')
	surface: {
		DEFAULT: withOpacity('--color-surface'),
		on: {
			DEFAULT: withOpacity('--color-surface-on'),
			inverse: {
				DEFAULT: withOpacity('--color-surface-inverse-on'),
			},
		},
		// Neutral variant tones
		variant: {
			DEFAULT: withOpacity('--color-surface-variant'),
			on: {
				DEFAULT: withOpacity('--color-surface-variant-on'),
			},
		},
		foreground: withOpacity('--color-surface-on'),
	},

	// Background tones
	background: {
		DEFAULT: withOpacity('--color-background'),
		on: {
			DEFAULT: withOpacity('--color-background-on'),
		},
		foreground: withOpacity('--color-background-on'),
	},

	outline: {
		DEFAULT: withOpacity('--color-outline'),
		variant: {
			DEFAULT: withOpacity('--color-outline-variant'),
		},
		foreground: withOpacity('--color-outline'),
	},

	// Error tones
	error: {
		DEFAULT: withOpacity('--color-error'),
		on: {
			DEFAULT: withOpacity('--color-error-on'),
		},
		container: {
			DEFAULT: withOpacity('--color-error-container'),
			on: {
				DEFAULT: withOpacity('--color-error-container-on'),
			},
		},
		foreground: withOpacity('--color-error-on'),
	},

	// Success tones (md3 didn't produce the extended color but secondary color is close)
	success: {
		DEFAULT: withOpacity('--color-secondary'),
		on: {
			DEFAULT: withOpacity('--color-secondary-on'),
		},
		container: {
			DEFAULT: withOpacity('--color-secondary-container'),
			on: {
				DEFAULT: withOpacity('--color-secondary-container-on'),
			},
		},
		foreground: withOpacity('--color-secondary-on'),
	},

	// shadcn aliases
	foreground: withOpacity('--color-background-on'),
	accent: withOpacity('--color-tertiary'),
	border: withOpacity('--color-primary'),
	input: withOpacity('--color-primary'),
	ring: withOpacity('--color-primary'),

	destructive: {
		DEFAULT: withOpacity('--color-error'),
		foreground: withOpacity('--color-error-on'),
	},
	muted: {
		DEFAULT: withOpacity('--color-surface-variant'),
		foreground: withOpacity('--color-surface-variant-on'),
	},
	popover: {
		DEFAULT: withOpacity('--color-surface'),
		foreground: withOpacity('--color-surface-on'),
	},
	card: {
		DEFAULT: withOpacity('--color-primary'),
		foreground: withOpacity('--color-surface-on'),
	},
};

export default colors;
