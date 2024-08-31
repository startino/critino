import * as Icons from 'lucide-svelte';
import type { Icon } from 'lucide-svelte';
import type { ComponentType } from 'svelte';

export type Route = {
	title: string;
	label: string;
	icon: ComponentType<Icon>;
	variant: 'default' | 'ghost';
};

export const primaryRoutes: Route[] = [
	{
		title: 'Home',
		label: null,
		icon: Icons.House,
		variant: 'ghost',
	},
	{
		title: 'Projects',
		label: null,
		icon: Icons.PanelsTopLeft,
		variant: 'ghost',
	},
];

export const teamRoutes: Route[] = [
	{
		title: 'Team',
		label: null,
		icon: Icons.Building2,
		variant: 'ghost',
	},
	{
		title: 'Members',
		label: null,
		icon: Icons.Users,
		variant: 'ghost',
	},
	{
		title: 'Settings',
		label: null,
		icon: Icons.Settings,
		variant: 'ghost',
	},
];

export const profileRoutes: Route[] = [
	{
		title: 'Profile',
		label: null,
		icon: Icons.User,
		variant: 'ghost',
	},
	{
		title: 'Settings',
		label: null,
		icon: Icons.Settings,
		variant: 'ghost',
	},
];
