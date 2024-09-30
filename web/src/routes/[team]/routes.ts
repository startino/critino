import * as Icons from 'lucide-svelte';
import type { Route } from '$lib/types/routes';
import type { Team } from '$lib/supabase';
import type { Tables } from '$lib/supabase';

export const primaryRoutes = (team: Team, environments: Tables<'environments'>[]): Route[] => [
	{
		title: 'Environments',
		label: environments.length.toString(),
		href: `/${team.name}`,
		icon: Icons.Orbit,
		variant: 'ghost',
	},
];

export const teamRoutes = (team: Team): Route[] => [
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
		href: `/${team.name}/settings`,
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
