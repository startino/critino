import type { User } from '@supabase/supabase-js';
import { error, type Handle } from '@sveltejs/kit';
import { createServerClient } from '$lib/supabase';
import { sequence } from '@sveltejs/kit/hooks';

export const supabase: Handle = async ({ event, resolve }) => {
	event.locals.supabase = createServerClient(event);

	event.locals.getUser = async (code: string | null = null) => {
		const getExistingUserOrCreateAnonymousUser = async (code: string | null) => {
			const {
				// tries to get the profile -> creates a profile
				data: { user },
				error: eUser,
			} = await event.locals.supabase.auth.getUser();

			if (code && !user) {
				await event.locals.supabase.auth.exchangeCodeForSession(code);
			}

			if (user) {
				return user;
			}

			const { data: newUser, error: eNewUser } = await event.locals.supabase.auth
				.signInAnonymously()
				.then((r) => {
					return { data: r.data.user, error: r.error };
				});

			if (!newUser || eNewUser) {
				const message = `Error fetching existing user: ${JSON.stringify(eUser, null, 2)}.\nError creating anonymous user: ${JSON.stringify(eNewUser, null, 2)}`;

				console.error(message);
				throw error(500, message);
			}

			return newUser;
		};

		const getExistingProfileOrCreateNewProfile = async (user: User) => {
			const { data: profile, error: eProfile } = await event.locals.supabase
				.from('profiles')
				.select('*')
				.eq('id', user.id)
				.single();

			if (profile) {
				return profile;
			}

			const { data: newProfile, error: eNewProfile } = await event.locals.supabase
				.from('profiles')
				.insert({
					id: user.id,
				})
				.select()
				.single();

			if (!newProfile || eNewProfile) {
				const message = `Error fetching existing profile: ${JSON.stringify(eProfile, null, 2)}.\nError creating anonymous profile: ${JSON.stringify(eNewProfile, null, 2)}`;

				console.error(message);
				throw error(500, message);
			}

			return newProfile;
		};

		if (event.url.pathname.startsWith('/api')) {
			return resolve(event);
		}

		try {
			const user = await getExistingUserOrCreateAnonymousUser(code);

			const profile = await getExistingProfileOrCreateNewProfile(user);

			return { ...user, ...profile };
		} catch (e) {
			console.error(JSON.stringify(e, null, 2));
			return null;
		}
	};

	return resolve(event, {
		filterSerializedResponseHeaders(name) {
			/**
			 * Supabase libraries use the `content-range` and `x-supabase-api-version`
			 * headers, so we need to tell SvelteKit to pass it through.
			 */
			return name === 'content-range' || name === 'x-supabase-api-version';
		},
	});
};

const authGuard: Handle = async ({ event, resolve }) => {
	if (event.url.pathname.startsWith('/api')) {
		return resolve(event);
	}

	const user = await event.locals.getUser();

	event.locals.user = user;

	return resolve(event);
};

const apiGuard: Handle = async ({ event, resolve }) => {
	if (event.request.method === 'OPTIONS') {
		// Preflight request. Reply successfully:
		return new Response(null, {
			headers: {
				'Access-Control-Allow-Origin': '*',
				'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
				'Access-Control-Allow-Headers': '*',
			},
		});
	}

	const response = await resolve(event);
	if (event.url.pathname.startsWith('/api')) {
		response.headers.append('Access-Control-Allow-Credentials', 'true');
		response.headers.append('Access-Control-Allow-Methods', '*');
		response.headers.append('Access-Control-Allow-Origin', `*`);
		response.headers.append('Access-Control-Allow-Headers', `*`);
	}
	return response;
};

export const handle: Handle = sequence(supabase, authGuard, apiGuard);
