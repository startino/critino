import { createBrowserClient } from '$lib/supabase/clients';
import type { Database, Json } from '$lib/supabase/database.types';
export { createBrowserClient, createServerClient } from '$lib/supabase/clients';
export const supabase = createBrowserClient();

type Tables = Database['public']['Tables'];
type Enums = Database['public']['Enums'];
type Views = Database['public']['Views'];
type Functions = Database['public']['Functions'];
type CompositeTypes = Database['public']['CompositeTypes'];

export type { Tables, Enums, Views, Functions, CompositeTypes, Json };

type Profile = Tables['profiles']['Row'];
type Team = Tables['teams']['Row'];
type Environment = Tables['environments']['Row'];
type Workflow = Tables['workflows']['Row'];
type Agent = Tables['agents']['Row'];
type Critique = Tables['critiques']['Row'];

export type { Database, Profile, Team, Environment, Workflow, Agent, Critique };
