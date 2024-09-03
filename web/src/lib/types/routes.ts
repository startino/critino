import type { Icon } from 'lucide-svelte';
import type { ComponentType } from 'svelte';

export type Route = {
	title: string;
	label: string | null;
	href: string;
	icon: ComponentType<Icon>;
	variant: 'default' | 'ghost';
};
