<script lang="ts">
	import { goto } from '$app/navigation';
	import { EntityControlGrid } from '$lib/components/ui/entity-control-grid';
	import { Typography } from '$lib/components/ui/typography';
	import { type Tables } from '$lib/supabase';

	export let data;

	$: ({ params, workflows } = data);
</script>

<Typography class="p-4 text-left" variant="headline-lg">
	{params.env?.toString().split('/').pop()}'s workflows
</Typography>

<EntityControlGrid
	on:click={async ({ detail: workflow }: CustomEvent<Tables<'environments'>>) => {
		await goto(`workflows/${workflow.name}`, {
			replaceState: true,
			invalidateAll: true,
		});
	}}
	name="workflow"
	entities={workflows}
/>
