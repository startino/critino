import { critiqueSchema } from '$lib/schema.js';
import { error } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';

export const load = async ({ params, parent, locals: { user, supabase } }) => {
	const { team, environment } = await parent();

	const { data: workflow, error: eWorkflow } = await supabase
		.from('workflows')
		.select('*')
		.eq('team_name', team.name)
		.eq('name', params.workflow)
		.single();

	if (!workflow || eWorkflow) {
		const message = `Error fetching workflow: ${eWorkflow.message}`;
		console.error(message);
		throw error(500, message);
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
