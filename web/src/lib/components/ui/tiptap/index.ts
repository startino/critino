import { tv } from 'tailwind-variants';
import Root from './tiptap.svelte';
import type { HTMLParamAttributes } from 'svelte/elements';

const variants = tv({
	base: 'min-w-[1.5rem] max-w-none w-full block prose prose-sm prose-main relative',
});

type Content = string;
type Editable = boolean;

type Props = {
	class?: HTMLParamAttributes['class'];
	editable?: Editable;
	content: Content;
};

export {
	Root,
	type Props,
	//
	Root as TipTap,
	type Props as TipTapProps,
	variants,
};
