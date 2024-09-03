<script lang="ts">
	import { Typography } from '$lib/components/ui/typography';
	import { type Props } from '.';
	import { cn } from '$lib/utils';

	type $$Props = Props;

	export let crumbs: $$Props['crumbs'];

	let className: $$Props['class'] = undefined;
	export { className as class };
</script>

<div class="absolute left-0 right-0 top-0 h-14 w-full flex-col items-center justify-center px-1">
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
					<a class="rounded-lg px-2 pb-0.5 hover:bg-surface-variant/40" href={crumb.href}>
						{crumb.name}
					</a>
				{:else}
					<span class="cursor-default rounded-lg px-2 pb-0.5">{crumb.name}</span>
				{/if}
			{/each}
		</Typography>
	</div>
</div>
