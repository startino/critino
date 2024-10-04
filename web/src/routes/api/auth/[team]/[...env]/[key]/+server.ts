import api from '$lib/api';
import { json } from '@sveltejs/kit';

export const GET = async ({ params, url }) => {
	console.log('GET /api/auth/[team]/[...env]/[key]/+server', params);

	const rParams = {
		query: {
			team_name: params.team,
			parent_name: url.searchParams.get('parent') ?? null,
		},
		path: { name: params.env },
		header: {
			'x-critino-key': params.key,
		},
	};

	console.log('params', rParams);

	const authResponse = await api.GET('/auth/environment/{name}', { params: rParams });

	console.log('api auth respons', authResponse);

	const status = authResponse.response.status;

	return json(authResponse.response, { status });
};
