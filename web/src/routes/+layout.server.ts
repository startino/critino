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

	let team_id = cookies.get('team') as string | null;

	if (!team_id) {
		const message = `Error getting team cookie. Using first team.`;
		console.error(message);
		if (!teams[0]) {
			throw error(500, `No teams exist`);
		}
		cookies.set('team', teams[0].id, { path: '/' });

		team_id = teams[0].id;
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

	console.log('teams', JSON.stringify(teams, null, 2));
	return {
		team,
		teams,
		user,
		cookies: cookies.getAll(),
	};
};
