import type { Database, Profile } from '$lib/supabase';
import { SupabaseClient } from '@supabase/supabase-js';

declare global {
	namespace App {
		// interface Error {}
		interface Locals {
			supabase: SupabaseClient<Database>;
			user: (User & Profile) | null;
			getUser(): Promise<(User & Profile) | null>;
		}
		interface PageData {
			user: (User & Profile) | null;
		}
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
