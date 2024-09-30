import * as Icons from 'lucide-svelte';
import type { Route } from '$lib/types/routes';
import type { Tables } from '$lib/supabase';

export const primaryRoutes = (
	team: Tables<'teams'>,
	environments: Tables<'environments'>[],
	environment: Tables<'environments'>,
	workflows: Tables<'workflows'>[]
): Route[] => [
	{
		title: 'Environments',
		label: environments.length.toString(),
		href: `/${team.name}/${environment.name}`,
		icon: Icons.Orbit,
		variant: 'ghost',
	},
	{
		title: 'Workflows',
		label: workflows.length.toString(),
		href: `/${team.name}/${environment.name}/workflows`,
		icon: Icons.Workflow,
		variant: 'ghost',
	},
	{
		title: 'Settings',
		label: null,
		href: `/${team.name}/${environment.name}/settings`,
		icon: Icons.Settings,
		variant: 'ghost',
	},
];
