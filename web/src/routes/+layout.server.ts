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

	let team_name = cookies.get('team') as string | null;

	if (!team_name) {
		const message = `Error getting team cookie. Using first team.`;
		console.error(message);
		if (!teams[0]) {
			throw error(500, `No teams exist`);
		}
		cookies.set('team', teams[0].name, { path: '/' });

		team_name = teams[0].name;
	}

	let { data: team, error: eTeam } = await supabase
		.from('teams')
		.select('*')
		.eq('name', team_name)
		.single();

	if (!team || eTeam) {
		const message = `Error fetching team: ${JSON.stringify(eTeam, null, 2)}`;
		console.error(message);

		if (!teams[0]) {
			throw error(500, `No teams exist`);
		}
		cookies.set('team', teams[0].name, { path: '/' });

		team_name = teams[0].name;

		const { data: team2, error: eTeam2 } = await supabase
			.from('teams')
			.select('*')
			.eq('name', team_name)
			.single();

		if (!team2 || eTeam2) {
			const message = `Error fetching team2: ${JSON.stringify(eTeam2, null, 2)}`;
			console.error(message);
			throw error(500, message);
		}

		team = team2;
	}

	console.log('teams', JSON.stringify(teams, null, 2));
	return {
		team,
		teams,
		user,
		cookies: cookies.getAll(),
	};
};
