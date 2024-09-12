<script lang="ts">
	import { Separator } from '$lib/components/ui/separator';
	import Sidepanel from './sidepanel.svelte';

	export let data;

	const { user, supabase, team, teams } = data;
</script>

<main class="flex h-screen w-screen items-stretch bg-background text-background-on">
	<Sidepanel {user} {supabase} {team} {teams} />
	<Separator orientation="vertical" class="ml-0 pl-0 opacity-20 " />

	<div class="relative flex w-full flex-col overflow-hidden text-nowrap">
		<slot />
	</div>
</main>
