import api from '$lib/api';
import type { Tables } from '$lib/supabase/database.types.js';
import { sluggify } from '$lib/utils';
import { error, type Cookies } from '@sveltejs/kit';

export const load = async ({ url, cookies, parent, params, locals: { supabase } }) => {
	const { data: workflows, error: eWorkflows } = await supabase
		.from('workflows')
		.select('*')
		.eq('team_name', params.team)
		.eq('environment_name', params.env)
		.order('name', { ascending: false });

	if (!workflows || eWorkflows) {
		const message = `Error fetching workflows: ${JSON.stringify(eWorkflows, null, 2)}`;
		console.error(message);
		throw error(500, message);
	}

	const environment = (await parent()).environments.find(
		(env) => sluggify(env.name) === sluggify(params.env)
	);

	if (!environment) {
		throw error(404, `Environment not found: ${params.env}`);
	}

	const getKey = (url: URL, cookies: Cookies, environment: Tables<'environments'>): string => {
		console.log('getKey', url, cookies, environment);
		const searchKey = url.searchParams.get('key');
		if (searchKey) {
			const cookieKey = `key-${environment.team_name}-${environment.name}`;
			cookies.set(cookieKey, searchKey, { path: '/', secure: false });
			console.log(`Set cookie: ${cookieKey} = ${searchKey}`);
			return searchKey;
		}

		const segments = environment.name.split('/');
		let key: string | undefined = '';

		for (let i = segments.length; i >= 0; i--) {
			const envSegment = segments.slice(0, i).join('/');
			const currentKey = `key-${environment.team_name}${envSegment ? '-' + envSegment : ''}`;
			key = cookies.get(currentKey);
			console.log(`Get cookie: ${currentKey}, key: ${key}`);
			if (key) return key;
		}

		return '';
	};

	const key = getKey(url, cookies, environment);

	const rParams = {
		query: {
			team_name: environment.team_name,
			parent_name:
				environment.name.split('/').length === 1
					? null
					: environment.name.split('/').slice(0, -1).join('/'),
		},
		path: { name: environment.name.split('/').pop() },
		header: {
			'x-critino-key': key,
		},
	};

	console.log('rParams', rParams);
	const authResponse = await api.GET('/auth/environment/{name}', {
		params: rParams,
	});
	console.log('authResponse', JSON.stringify(authResponse, null, 2));

	const authenticated = authResponse.response.status === 200;

	return {
		authenticated,
		workflows,
		environment,
	};
};
