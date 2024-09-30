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

		return {
			form,
		};
	},
};
