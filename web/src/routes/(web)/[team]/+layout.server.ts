import { error } from '@sveltejs/kit';

export const load = async ({ params, locals: { supabase } }) => {
	const { data: team, error: eTeam } = await supabase
		.from('teams')
		.select('*')
		.eq('name', params.team)
		.single();

	if (!team || eTeam) {
		const message = `Error fetching team: ${eTeam.message}`;
		console.error(message);
		throw error(500, message);
	}

	return {
		team,
	};
};
