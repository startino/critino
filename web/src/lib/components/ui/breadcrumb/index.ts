import type { HTMLParamAttributes } from 'svelte/elements';
import Root from './breadcrumb.svelte';

type Props = {
	crumbs: { name: string; href?: string }[];
	class?: HTMLParamAttributes['class'];
};

export {
	Root,
	type Props,
	//
	Root as Breadcrumb,
	type Props as BreadcrumbProps,
};
