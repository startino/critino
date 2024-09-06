import { error, redirect } from '@sveltejs/kit';

export const load = async ({ cookies, parent, locals: { user, supabase } }) => {
	const { team } = await parent();

	const { data: projects, error: eProjects } = await supabase
		.from('projects')
		.select('*')
		.eq('team_name', team.name)
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
