<script lang="ts">
	import { Typography } from '$lib/components/ui/typography';

	export let crumbs: { name: string; href: string }[];
</script>

<Typography as="h1" variant="body-lg" class="flex items-center justify-center">
	{#each crumbs as crumb, index (crumb)}
		{#if index > 0}
			<span class="px-4 text-2xl opacity-30">/</span>
		{/if}
		<a href={crumb.href}>{crumb.name}</a>
	{/each}
</Typography>
