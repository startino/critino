import { type VariantProps, tv } from 'tailwind-variants';
import Root from './typography.svelte';
import type { HTMLParamAttributes } from 'svelte/elements';

const typographyVariants = tv({
	base: 'block text-inherit antialiased m-0 sm:m-0',
	variants: {
		variant: {
			'display-lg': 'text-[4.0rem] font-semibold leading-tight',
			'display-md': 'text-[3.2rem] font-semibold leading-[1.3]',
			'display-sm': 'text-[2.5rem] font-semibold leading-snug',
			'headline-lg': 'text-[2.3rem] font-semibold leading-snug',
			'headline-md': 'text-[2.0rem] font-semibold leading-snug',
			'headline-sm': 'text-[1.7rem] font-semibold leading-relaxed',
			'title-lg': 'text-[1.6rem] leading-[1.88]',
			'title-md': 'text-lg leading-[1.9]',
			'title-sm': 'text-base leading-relaxed',
			'body-lg': 'text-lg font-light leading-relaxed',
			'body-md': 'text-base font-light leading-relaxed',
			'body-sm': 'text-sm font-light leading-normal',
		},
		overflow: {
			ellipsis: 'overflow-hidden text-ellipsis whitespace-nowrap',
			wrap: 'text-wrap',
		},
	},
	defaultVariants: {
		variant: 'body-md',
		overflow: 'wrap',
	},
});

type As = string;
type Variant = VariantProps<typeof typographyVariants>['variant'];
type Overflow = VariantProps<typeof typographyVariants>['overflow'];

type Props = {
	as?: As;
	variant?: Variant;
	overflow?: Overflow;
	class?: HTMLParamAttributes['class'];
};

export {
	Root,
	type Props,
	//
	Root as Typography,
	type Props as TypographyProps,
	typographyVariants,
};
