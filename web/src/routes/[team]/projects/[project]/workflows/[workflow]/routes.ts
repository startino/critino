import * as Icons from 'lucide-svelte';
import type { Route } from '$lib/types/routes';
import type { Critique, Agent, Project, Workflow, Team } from '$lib/supabase';

export const primaryRoutes = (
	team: Team,
	project: Project,
	workflow: Workflow,
	agents: Agent[],
	critiques: Critique[]
): Route[] => [
	{
		title: 'Critiques',
		label: critiques.length.toString(),
		href: `/${team.name}/projects/${project.name}/workflows/${workflow.name}/critiques`,
		icon: Icons.ListTodo,
		variant: 'ghost',
	},
	// {
	// 	title: 'Agents',
	// 	label: agents.length.toString(),
	// 	href: `/${team.name}/projects/${project.name}/workflows/${workflow.name}/agents`,
	// 	icon: Icons.Bot,
	// 	variant: 'ghost',
	// },
	// {
	// 	title: 'Endpoints',
	// 	label: null,
	// 	href: `/${team.name}/projects/${project.name}/workflows/${workflow.name}/endpoints`,
	// 	icon: Icons.Unplug,
	// 	variant: 'ghost',
	// },
];
