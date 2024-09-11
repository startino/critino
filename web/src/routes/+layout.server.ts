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

	let { data: team, error: eTeam } = await supabase
		.from('teams')
		.select('*')
		.eq('name', user.selected_team)
		.single();

	if (!team || eTeam) {
		const message = `Error fetching team: ${JSON.stringify(eTeam, null, 2)}`;
		console.error(message);

		if (!teams[0]) {
			throw error(500, `No teams exist`);
		}
		cookies.set('team', teams[0].name, { path: '/' });

		user.selected_team = teams[0].name;

		const { data: team2, error: eTeam2 } = await supabase
			.from('teams')
			.select('*')
			.eq('name', user.selected_team)
			.single();

		if (!team2 || eTeam2) {
			const message = `Error fetching team2: ${JSON.stringify(eTeam2, null, 2)}`;
			console.error(message);
			throw error(500, message);
		}

		team = team2;
	}

	console.log('routes/+layout.server.ts teams', JSON.stringify(teams, null, 2));
	console.log('routes/+layout.server.ts team', JSON.stringify(team, null, 2));
	return {
		team,
		teams,
		user,
		cookies: cookies.getAll(),
	};
};
