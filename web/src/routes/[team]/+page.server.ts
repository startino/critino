import { fail, error, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { formSchema } from './schema';

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
		form: await superValidate(zod(formSchema)),
		team,
		environments,
	};
};

export const actions = {
	default: async (event) => {
		const form = await superValidate(event, zod(formSchema));
		if (!form.valid) {
			return fail(400, {
				form,
			});
		}

		const {
			params,
			locals: { supabase },
		} = event;

		const { error: eEnvironment } = await supabase.from('environments').insert({
			name: form.data.name,
			description: form.data.description,
			team_name: params.team,
			parent_name: null,
		});

		if (eEnvironment) {
			console.error(
				`Error creating new environment ${JSON.stringify(eEnvironment, null, 2)}`
			);
			return fail(500, {
				form,
			});
		}

		return {
			form,
		};
	},
};
