import { critiqueSchema } from '$lib/schema.js';
import { error, fail, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';

export const load = async ({ params, parent, locals: { user, supabase } }) => {
	const { team, project } = await parent();

	const { data: critique, error: eCritique } = await supabase
		.from('critiques')
		.select('*')
		.eq('id', params.critique)
		.single();

	if (!critique || eCritique) {
		const message = `Error fetching critique: ${eCritique.message}`;
		console.error(message);
		throw error(500, message);
	}

	const { data: agent, error: eAgent } = await supabase
		.from('agents')
		.select('*')
		.eq('name', critique.agent_name)
		.single();

	if (!agent || eAgent) {
		const message = `Error fetching agent: ${eAgent.message}`;
		console.error(message);
		throw error(500, message);
	}

	const forms = {
		critique: await superValidate(zod(critiqueSchema)),
	};

	return {
		team,
		project,
		agent,
		critique,
		forms,
	};
};

export const actions = {
	default: async ({ request, locals: { supabase } }) => {
		const form = await superValidate(request, zod(critiqueSchema));

		if (!form.valid) {
			return fail(400, { form });
		}

		const review = await supabase
			.from('critiques')
			.update(form.data)
			.eq('id', form.data.id)
			.single();

		if (review) {
			throw redirect(303, '?success');
		}
	},
};
