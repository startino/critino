import { environmentSchema, workflowSchema } from '$lib/schema';
import { error } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';

export const load = async ({ params, locals: { supabase } }) => {
	const { data: team, error: eTeam } = await supabase
		.from('teams')
		.select('*')
		.eq('name', params.team)
		.single();

	if (!team || eTeam) {
		const message = `Error fetching team: ${JSON.stringify(eTeam, null, 2)}`;
		console.error(message);
		throw error(500, message);
	}

	const { data: environments, error: eEnvironments } = await supabase
		.from('environments')
		.select('*')
		.eq('team_name', team.name)
		.order('name', { ascending: false });

	if (!environments || eEnvironments) {
		const message = `Error fetching environments: ${JSON.stringify(eEnvironments, null, 2)}`;
		console.error(message);
		throw error(500, message);
	}

	return {
		form: {
			environment: await superValidate(zod(environmentSchema)),
			workflow: await superValidate(zod(workflowSchema)),
		},
		team,
		environments,
		params,
	};
};
