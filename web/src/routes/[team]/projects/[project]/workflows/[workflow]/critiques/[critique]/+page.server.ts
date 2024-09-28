import { critiqueSchema } from '$lib/schema.js';
import { error, fail, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';

export const load = async ({ params, parent, locals: { supabase } }) => {
	const { team, environment, agents, critiques } = await parent();

	const critique = critiques.find((c) => c.id === params.critique);

	if (!critique) {
		const message = `Critique ${params.critique} not found`;
		console.error(message);
		throw error(500, message);
	}

	const agent = agents.find(
		(a) =>
			a.name === critique.agent_name &&
			a.workflow_name === critique.workflow_name &&
			a.environment_name === critique.environment_name &&
			a.team_name === critique.team_name
	);

	if (!agent) {
		const message = `Agent ${critique.agent_name} not found`;
		console.error(message);
		throw error(500, message);
	}

	const forms = {
		critique: await superValidate(zod(critiqueSchema)),
	};

	return {
		team,
		environment,
		agent,
		critique,
		forms,
	};
};
