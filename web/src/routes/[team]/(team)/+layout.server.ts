import api from '$lib/api';
import type { Tables } from '$lib/supabase/database.types.js';
import { type Cookies } from '@sveltejs/kit';

export const load = async ({ url, cookies, parent, params, locals: { supabase } }) => {
	const getKey = (url: URL, cookies: Cookies, team: Tables<'teams'>): string => {
		const searchKey = url.searchParams.get('key');
		if (searchKey) {
			const cookieKey = `key-${team.name}`;
			cookies.set(cookieKey, searchKey, { path: '/', secure: false });
			console.log(`Set cookie: ${cookieKey} = ${searchKey}`);
			return searchKey;
		}

		let key = cookies.get(`key-${team.name}`);
		console.log(`Get cookie: key-${team.name}, key: ${key}`);
		if (key) return key;
		return '';
	};

	const team = (await parent()).team;

	const key = getKey(url, cookies, team);

	const rParams = {
		path: { name: team.name },
		header: {
			'x-critino-key': key,
		},
	};

	console.log('rParams', rParams);
	const authResponse = await api.GET('/auth/team/{name}', {
		params: rParams,
	});
	console.log('authResponse', JSON.stringify(authResponse, null, 2));

	const authenticated = authResponse.response.status === 200;

	return {
		authenticated,
	};
};
