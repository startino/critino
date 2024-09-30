import * as Icons from 'lucide-svelte';
import type { Route } from '$lib/types/routes';
import type { Tables } from '$lib/supabase';

export const primaryRoutes = (
	team: Tables<'teams'>,
	environment: Tables<'environments'>,
	workflows: Tables<'workflows'>[]
): Route[] => [
	{
		title: 'Workflows',
		label: workflows.length.toString(),
		href: `/${team.name}/environments/${environment.name}/workflows`,
		icon: Icons.Workflow,
		variant: 'ghost',
	},
	// {
	// 	title: 'Agents',
	// 	label: agents.length.toString(),
	// 	href: `/${team.name}/environments/${environment.name}/workflows/${workflow.name}/agents`,
	// 	icon: Icons.Bot,
	// 	variant: 'ghost',
	// },
	// {
	// 	title: 'Endpoints',
	// 	label: null,
	// 	href: `/${team.name}/environments/${environment.name}/workflows/${workflow.name}/endpoints`,
	// 	icon: Icons.Unplug,
	// 	variant: 'ghost',
	// },
];
