import { error } from '@sveltejs/kit';

export const load = async ({ cookies, locals: { user, supabase } }) => {
	const { data: teams, error: eTeams } = await supabase
		.from('teams')
		.select('*')
		.order('name', { ascending: false });

	if (!teams || eTeams) {
		const message = `Error fetching teams: ${eTeams.message}`;
		console.error(message);
		throw error(500, message);
	}

	return {
		teams,
		user,
		cookies: cookies.getAll(),
	};
};
