import { error } from '@sveltejs/kit';

export const load = async ({ parent, params, locals: { supabase } }) => {
	const { data: workflows, error: eWorkflows } = await supabase
		.from('workflows')
		.select('*')
		.eq('team_name', params.team)
		.eq('environment_name', params.env)
		.order('name', { ascending: false });

	if (!workflows || eWorkflows) {
		const message = `Error fetching workflows: ${JSON.stringify(eWorkflows, null, 2)}`;
		console.error(message);
		throw error(500, message);
	}
	const environment = (await parent()).environments.find((env) => env.name === params.env);

	if (!environment) {
		throw error(404, 'Environment not found');
	}

	return {
		workflows,
		environment,
	};
};
