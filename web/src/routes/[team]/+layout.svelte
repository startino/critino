<script lang="ts">
	import { Separator } from '$lib/components/ui/separator';
	import Sidepanel from './sidepanel.svelte';

	export let data;

	$: ({ supabase, team, teams, environments: allEnvironments } = data);

	$: environments = allEnvironments.filter((env) => !env.name.includes('/'));
</script>

<main class="flex h-screen w-screen items-stretch bg-background text-background-on">
	<Sidepanel {supabase} {team} {teams} {environments} />
	<Separator orientation="vertical" class="ml-0 pl-0 opacity-20 " />

	<div class="relative flex w-full flex-col overflow-hidden text-nowrap">
		<slot />
	</div>
</main>
