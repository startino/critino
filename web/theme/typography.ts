import colorConfig from './color';

const typography = () => {
	return {
		main: {
			css: {
				'--tw-prose-body': colorConfig.background.on.DEFAULT,
				'--tw-prose-headings': colorConfig.background.on.DEFAULT,
				'--tw-prose-lead': colorConfig.background.on.DEFAULT,
				'--tw-prose-links': colorConfig.background.DEFAULT,
				'--tw-prose-bold': colorConfig.background.on.DEFAULT,
				'--tw-prose-counters': colorConfig.background.DEFAULT,
				'--tw-prose-bullets': colorConfig.background.DEFAULT,
				'--tw-prose-hr': colorConfig.background.DEFAULT,
				'--tw-prose-quotes': colorConfig.background.DEFAULT,
				'--tw-prose-quote-borders': colorConfig.background.DEFAULT,
				'--tw-prose-captions': colorConfig.background.DEFAULT,
				'--tw-prose-code': colorConfig.background.DEFAULT,
				'--tw-prose-pre-code': colorConfig.background.DEFAULT,
				'--tw-prose-pre-bg': 'rgb(0 0 0 / 50%)',
				'--tw-prose-th-borders': colorConfig.background.DEFAULT,
				'--tw-prose-td-borders': colorConfig.background.DEFAULT,
				'--tw-prose-invert-body': colorConfig.background.DEFAULT,
				'--tw-prose-invert-headings': colorConfig.background.DEFAULT,
				'--tw-prose-invert-lead': colorConfig.background.DEFAULT,
				'--tw-prose-invert-links': colorConfig.background.DEFAULT,
				'--tw-prose-invert-bold': colorConfig.background.DEFAULT,
				'--tw-prose-invert-counters': colorConfig.background.DEFAULT,
				'--tw-prose-invert-bullets': colorConfig.background.DEFAULT,
				'--tw-prose-invert-hr': colorConfig.background.DEFAULT,
				'--tw-prose-invert-lists': colorConfig.background.DEFAULT,
				'--tw-prose-invert-quotes': colorConfig.background.DEFAULT,
				'--tw-prose-invert-quote-borders': colorConfig.background.DEFAULT,
				'--tw-prose-invert-captions': colorConfig.background.DEFAULT,
				'--tw-prose-invert-code': colorConfig.background.DEFAULT,
				'--tw-prose-invert-pre-code': colorConfig.background.DEFAULT,
				'--tw-prose-invert-pre-bg': 'rgb(0 0 0 / 50%)',
				'--tw-prose-invert-th-borders': colorConfig.background.DEFAULT,
				'--tw-prose-invert-td-borders': colorConfig.background.DEFAULT,
			},
		},
	};
};

export default typography;
