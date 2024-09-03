<script lang="ts">
	import TeamSwitcher from './team-switcher.svelte';
	import Nav from '$lib/components/ui/nav.svelte';
	import { Separator } from '$lib/components/ui/separator';
	import { primaryRoutes, profileRoutes, teamRoutes } from './routes';
	import { Typography } from '$lib/components/ui/typography/index.js';
	import type { Team } from '$lib/supabase';

	export let teams: Team[];

	let isCollapsed = true;
</script>

<div
	role="navigation"
	on:mouseenter={() => (isCollapsed = false)}
	on:mouseleave={() =>
		setTimeout(() => {
			isCollapsed = true;
		}, 150)}
	class="group flex min-w-14 max-w-14 flex-col overflow-hidden text-nowrap transition-all duration-200 ease-in-out hover:min-w-52 hover:max-w-52"
>
	<div class="flex h-14 flex-col items-center justify-center px-1">
		<TeamSwitcher {isCollapsed} {teams} />
	</div>

	<Separator class="mt-0 pt-0 opacity-40" />

	<Nav routes={primaryRoutes} />

	<Separator
		class="ml-2 min-w-10 max-w-10 pt-0 opacity-40 transition-all duration-200 ease-in-out group-hover:min-w-48 group-hover:max-w-48"
	/>

	<div class="relative grid h-8">
		<Typography
			align="left"
			variant="body-lg"
			class="absolute bottom-0 left-0 right-0 top-0 h-full px-[1.45rem] py-2"
		>
			T
		</Typography>
		<Typography
			align="left"
			variant="body-lg"
			class="absolute bottom-0 left-0 right-0 top-0 h-full px-[1.45rem] py-2 opacity-0 transition-all duration-200 ease-in-out group-hover:opacity-100"
		>
			Team Management
		</Typography>
	</div>
	<Nav routes={teamRoutes} />

	<Separator
		class="ml-2 min-w-10 max-w-10 pt-0 opacity-40 transition-all duration-200 ease-in-out group-hover:min-w-48 group-hover:max-w-48"
	/>

	<div class="relative grid h-8">
		<Typography
			align="left"
			variant="body-lg"
			class="absolute bottom-0 left-0 right-0 top-0 h-full px-[1.45rem] py-2"
		>
			P
		</Typography>
		<Typography
			align="left"
			variant="body-lg"
			class="absolute bottom-0 left-0 right-0 top-0 h-full px-[1.45rem] py-2 opacity-0 transition-all duration-200 ease-in-out group-hover:opacity-100"
		>
			Profile Management
		</Typography>
	</div>
	<Nav routes={profileRoutes} />
</div>
