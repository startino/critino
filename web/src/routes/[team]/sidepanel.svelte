<script lang="ts">
	import Nav from '$lib/components/ui/nav.svelte';
	import { Separator } from '$lib/components/ui/separator';
	import { primaryRoutes, profileRoutes, teamRoutes } from './routes';
	import { Typography } from '$lib/components/ui/typography/index.js';
	import type { Database, Team } from '$lib/supabase';
	import type { SupabaseClient } from '@supabase/supabase-js';
	import TeamSwitcher from './team-switcher.svelte';
	import type { Tables } from '$lib/supabase';

	export let supabase: SupabaseClient<Database>;
	export let team: Team;
	export let teams: Team[];
	export let environments: Tables<'environments'>[];

	let isCollapsed = true;
</script>

<div
	role="navigation"
	on:mouseenter={() => (isCollapsed = false)}
	on:mouseleave={() =>
		setTimeout(() => {
			isCollapsed = true;
		}, 150)}
	class="group relative flex min-w-14 max-w-14 flex-col overflow-hidden text-nowrap transition-all duration-200 ease-in-out hover:min-w-52 hover:max-w-52"
>
	<div class="absolute left-0 right-0 top-0 flex h-14 flex-col items-center justify-center px-1">
		<TeamSwitcher {supabase} {isCollapsed} bind:selectedTeam={team} {teams} />
	</div>

	<Separator class="mt-14 opacity-20" />

	<Nav routes={primaryRoutes(team, environments)} />

	<Separator
		class="ml-2 min-w-10 max-w-10 pt-0 opacity-40 transition-all duration-200 ease-in-out group-hover:min-w-48 group-hover:max-w-48"
	/>

	<div class="relative grid h-8">
		<Typography
			variant="body-lg"
			class="absolute bottom-0 left-0 right-0 top-0 h-full px-[1.45rem] py-2 text-left"
		>
			T
		</Typography>
		<Typography
			variant="body-lg"
			class="absolute bottom-0 left-0 right-0 top-0 h-full px-[1.45rem] py-2 text-left opacity-0 transition-all duration-200 ease-in-out group-hover:opacity-100"
		>
			Team Management
		</Typography>
	</div>
	<Nav routes={teamRoutes(team)} />

	<Separator
		class="ml-2 min-w-10 max-w-10 pt-0 opacity-20 transition-all duration-200 ease-in-out group-hover:min-w-48 group-hover:max-w-48"
	/>

	<div class="relative grid h-8">
		<Typography
			variant="body-lg"
			class="absolute bottom-0 left-0 right-0 top-0 h-full px-[1.45rem] py-2 text-left"
		>
			P
		</Typography>
		<Typography
			variant="body-lg"
			class="absolute bottom-0 left-0 right-0 top-0 h-full px-[1.45rem] py-2 text-left opacity-0 transition-all duration-200 ease-in-out group-hover:opacity-100"
		>
			Profile Management
		</Typography>
	</div>
	<Nav routes={profileRoutes} />
</div>
