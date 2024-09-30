<script lang="ts">
	import { Breadcrumb } from '$lib/components/ui/breadcrumb/index.js';
	import { Separator } from '$lib/components/ui/separator';
	import Sidepanel from './sidepanel.svelte';

	export let data;

	const { user, supabase, team, teams, environments } = data;
</script>

<main class="flex h-screen w-screen items-stretch bg-background text-background-on">
	<Sidepanel {supabase} {team} {teams} {environments} />
	<Separator orientation="vertical" class="ml-0 pl-0 opacity-20 " />

	<div class="relative flex w-full flex-col overflow-hidden text-nowrap">
		<slot />
	</div>
</main>
