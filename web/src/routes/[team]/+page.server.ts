import { environmentSchema } from '$lib/schema';
import { fail } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';

export const actions = {
	default: async (event) => {
		const form = await superValidate(event, zod(environmentSchema));
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
			name: form.data.full_name,
			description: form.data.description,
			team_name: params.team,
			parent_name: form.data.parent_name,
		});

		if (eEnvironment) {
			console.error(
				`Error creating new environment\nError: ${JSON.stringify(eEnvironment, null, 2)}\nForm: ${JSON.stringify(form, null, 2)}`
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
