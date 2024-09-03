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

			if (eUser) {
				console.error(`Error retrieving user: ${JSON.stringify(eUser, null)}`);
			}

			if (user) {
				return user;
			}

			const { data: newUser, error: eNewUser } = await event.locals.supabase.auth
				.signInAnonymously()
				.then((r) => {
					return { data: r.data.user, error: r.error };
				});

			if (eNewUser) {
				console.error(
					`Error creating anonymous user: ${JSON.stringify(eNewUser, null, 2)}`
				);
			}

			if (newUser) {
				return newUser;
			}

			const message =
				'Failed to find or create user. Please report the issue and try again later.';

			console.error(message);
			throw error(500, message);
		};

		const getExistingProfileOrCreateNewProfile = async (user: User) => {
			const { data: profile, error: eProfile } = await event.locals.supabase
				.from('profiles')
				.select('*')
				.eq('id', user.id)
				.single();

			if (eProfile) {
				console.error(`Error retrieving profile: ${JSON.stringify(eProfile, null, 2)}`);
			}

			if (profile) {
				return profile;
			}

			const { data: newProfile, error: eProfile2 } = await event.locals.supabase
				.from('profiles')
				.insert({
					id: user.id,
				})
				.select()
				.single();

			if (eProfile2) {
				console.error(`Error making new profile: ${JSON.stringify(eProfile2, null, 2)}`);
			}

			if (newProfile) {
				return newProfile;
			}

			const message =
				'Failed to find or create profile. Please report the issue and try again later.';
			console.error(message);
			throw error(500, message);
		};

		if (event.url.pathname.startsWith('/api')) {
			return resolve(event);
		}

		const user = await getExistingUserOrCreateAnonymousUser(code);

		const profile = await getExistingProfileOrCreateNewProfile(user);

		return { ...user, ...profile };
	};

	/**
	 * Unlike `supabase.auth.getSession()`, which returns the session _without_
	 * validating the JWT, this function also calls `getUser()` to validate the
	 * JWT before returning the session.
	 */
	event.locals.getSession = async (code: string | null = null) => {
		const {
			data: { session },
		} = await event.locals.supabase.auth.getSession();
		if (!session) {
			return null;
		}

		const userProfile = await event.locals.getUser(code);
		if (!userProfile) {
			return null;
		}

		return { ...session, ...userProfile };
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
	// Apply CORS header for API routes
	if (event.url.pathname.startsWith('/api')) {
		// Required for CORS to work
		if (event.request.method === 'OPTIONS') {
			return new Response(null, {
				headers: {
					'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
					'Access-Control-Allow-Origin': '*',
					'Access-Control-Allow-Headers': '*',
				},
			});
		}
	}

	const response = await resolve(event);
	if (event.url.pathname.startsWith('/api')) {
		response.headers.append('Access-Control-Allow-Origin', `*`);
	}
	return response;
};
export const handle: Handle = sequence(supabase, authGuard, apiGuard);
