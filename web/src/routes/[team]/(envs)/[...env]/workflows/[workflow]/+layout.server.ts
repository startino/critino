import { sluggify } from '$lib/utils.js';
import { error } from '@sveltejs/kit';

export const load = async ({ params, parent, locals: { user, supabase } }) => {
	const { team, environment } = await parent();

	const workflow = (await parent()).workflows.find(
		(workflow) => sluggify(workflow.name) === sluggify(params.workflow)
	);

	if (!workflow) {
		throw error(404, `workflow not found: ${params.env}`);
	}

	const { data: agents, error: eAgents } = await supabase
		.from('agents')
		.select('*')
		.eq('team_name', team.name)
		.eq('environment_name', environment.name)
		.eq('workflow_name', workflow.name);

	if (!agents || eAgents) {
		const message = `Error fetching agents: ${eAgents.message}`;
		console.error(message);
		throw error(500, message);
	}

	const { data: critiques, error: eCritiques } = await supabase
		.from('critiques')
		.select('*')
		.eq('team_name', team.name)
		.eq('environment_name', environment.name)
		.eq('workflow_name', workflow.name);

	if (!critiques || eCritiques) {
		const message = `Error fetching critiques: ${eCritiques.message}`;
		console.error(message);
		throw error(500, message);
	}

	return {
		team,
		environment,
		workflow,
		agents,
		critiques,
	};
};
