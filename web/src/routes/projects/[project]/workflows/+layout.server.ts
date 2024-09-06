import { error, redirect } from '@sveltejs/kit';

export const load = async ({ params, parent, locals: { supabase } }) => {
	const { team } = await parent();

	const { data: project, error: eProject } = await supabase
		.from('projects')
		.select('*')
		.eq('team_name', team.name)
		.eq('name', params.project)
		.single();

	if (!project || eProject) {
		const message = `Error fetching project: ${eProject.message}`;
		console.error(message);
		throw error(500, message);
	}

	const { data: workflows, error: eWorkflows } = await supabase
		.from('workflows')
		.select('*')
		.eq('team_name', team.name)
		.eq('project_name', project.name);

	if (!workflows || eWorkflows) {
		const message = `Error fetching workflows: ${eWorkflows.message}`;
		console.error(message);
		throw error(500, message);
	}

	return {
		team,
		project,
		workflows,
	};
};
