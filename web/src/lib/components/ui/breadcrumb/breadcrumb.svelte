<script lang="ts">
	import { Typography } from '$lib/components/ui/typography';
	import { type Props } from '.';
	import { cn } from '$lib/utils';
	import { Separator } from '../separator';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	type $$Props = Props;

	let crumbs: { name: string; href?: string }[] = [];

	onMount(() => {
		if (browser) {
			crumbs = generateCrumbs(window.location.pathname);
		}
	});

	function generateCrumbs(url: string) {
		const segments = url.split('/').filter((segment) => segment);
		return segments.map((segment, index) => {
			const href = '/' + segments.slice(0, index + 1).join('/');
			return { name: segment, href };
		});
	}

	let className: $$Props['class'] = undefined;
	export { className as class };
</script>

<div class="absolute left-0 right-0 top-0 h-14 w-full flex-col items-center justify-center px-4">
	<div class="flex h-full w-full items-center justify-start">
		<Typography
			as="h1"
			variant="body-lg"
			class={cn('flex items-center justify-center', className)}
		>
			{#each crumbs as crumb, index (crumb)}
				{#if index > 0}
					<span class="px-4 text-2xl opacity-30">/</span>
				{/if}
				{#if crumb.href}
					<a
						class="overflow-hidden text-ellipsis rounded-lg px-2 pb-0.5 hover:bg-surface-variant/40"
						href={crumb.href}
					>
						{decodeURIComponent(crumb.name)}
					</a>
				{:else}
					<span class="cursor-default overflow-hidden rounded-lg px-2 pb-0.5">
						{crumb.name}
					</span>
				{/if}
			{/each}
		</Typography>
	</div>
</div>
<Separator class="mt-14 opacity-20" />
