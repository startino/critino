import { error } from '@sveltejs/kit';

export const load = async ({ params, locals: { user, supabase } }) => {
	const { data: project, error: eProject } = await supabase
		.from('projects')
		.select('*')
		.eq('id', params.project)
		.single();

	if (!project || eProject) {
		const message = `Error fetching project: ${eProject.message}`;
		console.error(message);
		throw error(500, message);
	}

	const { data: team, error: eTeam } = await supabase
		.from('teams')
		.select('*')
		.eq('id', project.team_id)
		.single();

	if (!team || eTeam) {
		const message = `Error fetching team: ${eTeam.message}`;
		console.error(message);
		throw error(500, message);
	}

	return {
		team,
		project,
	};
};
