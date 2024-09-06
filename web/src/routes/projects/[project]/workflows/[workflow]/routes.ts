import * as Icons from 'lucide-svelte';
import type { Route } from '$lib/types/routes';
import type { Critique, Agent, Project, Workflow } from '$lib/supabase';

export const primaryRoutes = (
	project: Project,
	workflow: Workflow,
	agents: Agent[],
	critiques: Critique[]
): Route[] => [
	{
		title: 'Critiques',
		label: critiques.length.toString(),
		href: `/projects/${project.name}/workflows/${workflow.name}/critiques`,
		icon: Icons.ListTodo,
		variant: 'ghost',
	},
	{
		title: 'Agents',
		label: agents.length.toString(),
		href: `/projects/${project.name}/workflows/${workflow.name}/agents`,
		icon: Icons.Bot,
		variant: 'ghost',
	},
	{
		title: 'Endpoints',
		label: null,
		href: `/projects/${project.name}/workflows/${workflow.name}/endpoints`,
		icon: Icons.Unplug,
		variant: 'ghost',
	},
];
