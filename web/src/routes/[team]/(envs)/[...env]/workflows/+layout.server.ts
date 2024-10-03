import { sluggify } from '$lib/utils.js';
import { error, redirect } from '@sveltejs/kit';

export const load = async ({ params, parent, locals: { supabase } }) => {
	const { team } = await parent();

	const environment = (await parent()).environments.find(
		(env) => sluggify(env.name) === sluggify(params.env)
	);

	if (!environment) {
		throw error(404, `Environment not found: ${params.env}`);
	}

	const { data: workflows, error: eWorkflows } = await supabase
		.from('workflows')
		.select('*')
		.eq('team_name', team.name)
		.eq('environment_name', environment.name);

	if (!workflows || eWorkflows) {
		const message = `Error fetching workflows: ${eWorkflows.message}`;
		console.error(message);
		throw error(500, message);
	}

	return {
		params,
		team,
		environment,
		workflows,
	};
};
