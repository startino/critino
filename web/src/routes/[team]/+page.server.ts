import { error, redirect } from '@sveltejs/kit';

export const load = async ({ parent }) => {
	const { teams } = await parent();

	throw redirect(303, teams[0].name + '/environments');
};
