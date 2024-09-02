<script lang="ts">
	import TeamSwitcher from './team-switcher.svelte';
	import Nav from './nav.svelte';
	import { Separator } from '$lib/components/ui/separator';
	import { primaryRoutes, profileRoutes, teamRoutes } from './routes';
	import { cn } from '$lib/utils';
	import { Typography } from '$lib/components/ui/typography/index.js';
	import type { Team } from '$lib/supabase';

	export let teams: Team[];

	let isCollapsed = true;
</script>

<div
	on:mouseenter={() => (isCollapsed = false)}
	on:mouseleave={() =>
		setTimeout(() => {
			isCollapsed = true;
		}, 150)}
	class="flex min-w-14 max-w-14 flex-col overflow-hidden text-nowrap transition-all duration-200 ease-in-out hover:min-w-52 hover:max-w-52"
>
	<div class={cn('flex h-14 flex-col items-center justify-center px-2')}>
		<TeamSwitcher {isCollapsed} {teams} />
	</div>
	<Separator class="mt-0 pt-0" />
	<Nav {isCollapsed} routes={primaryRoutes} />
	<Separator />
	<div class="grid gap-1 px-2">
		<Typography
			align="left"
			variant="body-lg"
			class={cn('self-center px-4 pt-2', isCollapsed ? 'block' : 'hidden')}
		>
			T
		</Typography>
		<Typography
			align="left"
			variant="body-lg"
			class={cn('px-4 pt-2', isCollapsed ? 'hidden' : 'block')}
		>
			Team Management
		</Typography>
	</div>
	<Nav {isCollapsed} routes={teamRoutes} />
	<Separator />

	<div class="grid gap-1 px-2">
		<Typography
			align="left"
			variant="body-lg"
			class={cn('px-3.5 pt-2', isCollapsed ? 'block' : 'hidden')}
		>
			P
		</Typography>
		<Typography
			align="left"
			variant="body-lg"
			class={cn('px-3.5 pt-2', isCollapsed ? 'hidden' : 'block')}
		>
			Profile Management
		</Typography>
	</div>
	<Nav {isCollapsed} routes={profileRoutes} />
</div>
