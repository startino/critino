import * as Icons from 'lucide-svelte';
import type { Icon } from 'lucide-svelte';
import type { ComponentType } from 'svelte';
import type { Route } from '$lib/types/routes';
import type { Team } from '$lib/supabase';

export const primaryRoutes = (team: Team): Route[] => [
	{
		title: 'Home',
		label: null,
		href: `/${team.name}`,
		icon: Icons.House,
		variant: 'ghost',
	},
	{
		title: 'Projects',
		label: null,
		href: `/${team.name}/projects`,
		icon: Icons.PanelsTopLeft,
		variant: 'ghost',
	},
];

export const teamRoutes: Route[] = [
	{
		title: 'Team',
		label: null,
		href: '',
		icon: Icons.Building2,
		variant: 'ghost',
	},
	{
		title: 'Members',
		label: null,
		href: '',
		icon: Icons.Users,
		variant: 'ghost',
	},
	{
		title: 'Settings',
		label: null,
		href: '',
		icon: Icons.Settings,
		variant: 'ghost',
	},
];

export const profileRoutes: Route[] = [
	{
		title: 'Profile',
		label: null,
		href: '',
		icon: Icons.User,
		variant: 'ghost',
	},
	{
		title: 'Settings',
		label: null,
		href: '',
		icon: Icons.Settings,
		variant: 'ghost',
	},
];
