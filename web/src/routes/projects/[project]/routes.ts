import * as Icons from 'lucide-svelte';
import type { Route } from '$lib/types/routes';
import type { Project } from '$lib/supabase';

export const primaryRoutes = (project: Project): Route[] => [
	{
		title: 'Critiques',
		label: null,
		href: `/projects/${project.name}/critiques`,
		icon: Icons.ListTodo,
		variant: 'ghost',
	},
	{
		title: 'Agents',
		label: null,
		href: `/projects/${project.name}/agents`,
		icon: Icons.Bot,
		variant: 'ghost',
	},
	{
		title: 'Endpoints',
		label: null,
		href: `/projects/${project.name}/endpoints`,
		icon: Icons.Unplug,
		variant: 'ghost',
	},
];
