import { error, redirect } from '@sveltejs/kit';

export const load = async ({ params, parent, locals: { supabase } }) => {
	const { team } = await parent();

	const { data: environment, error: eEnvironment } = await supabase
		.from('environments')
		.select('*')
		.eq('team_name', team.name)
		.eq('name', params.env)
		.single();

	if (!environment || eEnvironment) {
		const message = `Error fetching environment: ${eEnvironment.message}`;
		console.error(message);
		throw error(500, message);
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
