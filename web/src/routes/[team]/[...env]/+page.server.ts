import { redirect } from '@sveltejs/kit';

export const load = async ({ params }) => {
	return {
		params,
	};
};
