<script lang="ts">
	import { Typography } from '$lib/components/ui/typography';

	export let crumbs: string[];
</script>

<Typography as="h1" variant="body-lg" class="flex items-center justify-center">
	{#each crumbs as crumb, index (crumb)}
		{#if index > 0}
			<span class="px-4 text-2xl opacity-30">/</span>
		{/if}
		{crumb}
	{/each}
</Typography>
