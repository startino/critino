import { createBrowserClient } from '$lib/supabase/clients';
import type { Tables, Database, Json } from '$lib/supabase/database.types';
export { createBrowserClient, createServerClient } from '$lib/supabase/clients';
export const supabase = createBrowserClient();

type Enums = Database['public']['Enums'];
type Views = Database['public']['Views'];
type Functions = Database['public']['Functions'];
type CompositeTypes = Database['public']['CompositeTypes'];

export type { Tables, Enums, Views, Functions, CompositeTypes, Json };

type Profile = Tables<'profiles'>;
type Team = Tables<'teams'>;
type Environment = Tables<'environments'>;
type Workflow = Tables<'workflows'>;
type Agent = Tables<'agents'>;
type Critique = Tables<'critiques'>;

export type { Database, Profile, Team, Environment, Workflow, Agent, Critique };
