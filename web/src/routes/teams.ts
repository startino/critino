import type { Icon } from 'lucide-svelte';
import type { ComponentType } from 'svelte';
import * as Icons from '$lib/icons';

export type Team = {
	label: string;
	icon: ComponentType<Icon>;
};

export const teams: Team[] = [
	{
		label: 'Startino',
		icon: Icons.Startino,
	},
	{
		label: 'Critino',
		icon: Icons.Critino,
	},
];
