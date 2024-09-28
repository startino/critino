import { error, redirect } from '@sveltejs/kit';

export const load = async ({ parent, locals: { supabase } }) => {
	const { team } = await parent();

	const { data: environments, error: eEnvironments } = await supabase
		.from('environments')
		.select('*')
		.eq('team_name', team.name)
		.order('name', { ascending: false });

	if (!environments || eEnvironments) {
		const message = `Error fetching environments: ${eEnvironments.message}`;
		console.error(message);
		throw error(500, message);
	}

	return {
		team,
		environments,
	};
};
