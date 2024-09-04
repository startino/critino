import { error } from '@sveltejs/kit';

export const load = async ({ params, parent, locals: { user, supabase } }) => {
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

	const { data: agents, error: eAgents } = await supabase
		.from('agents')
		.select('*')
		.eq('team_name', team.name)
		.eq('project_name', project.name);

	if (!agents || eAgents) {
		const message = `Error fetching agents: ${eAgents.message}`;
		console.error(message);
		throw error(500, message);
	}

	const { data: critiques, error: eCritiques } = await supabase
		.from('critiques')
		.select('*')
		.eq('team_name', team.name)
		.eq('project_name', project.name);

	if (!critiques || eCritiques) {
		const message = `Error fetching critiques: ${eCritiques.message}`;
		console.error(message);
		throw error(500, message);
	}

	return {
		team,
		project,
		agents,
		critiques,
	};
};
