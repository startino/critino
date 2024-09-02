import { error, redirect } from '@sveltejs/kit';

export const load = async ({ cookies, locals: { user, supabase } }) => {
	const team_id = cookies.get('team') as string | null;

	if (!team_id) {
		const message = `Error getting team cookie`;
		console.error(message);
		throw redirect(303, '/');
	}

	const { data: team, error: eTeam } = await supabase
		.from('teams')
		.select('*')
		.eq('id', team_id)
		.single();

	if (!team || eTeam) {
		const message = `Error fetching team: ${eTeam.message}`;
		console.error(message);
		throw error(500, message);
	}

	const { data: projects, error: eProjects } = await supabase
		.from('projects')
		.select('*')
		.eq('team_id', team_id)
		.order('name', { ascending: false });

	if (!projects || eProjects) {
		const message = `Error fetching projects: ${eProjects.message}`;
		console.error(message);
		throw error(500, message);
	}

	return {
		team,
		projects,
	};
};
