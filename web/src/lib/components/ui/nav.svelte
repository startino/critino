<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import type { Route } from '$lib/types/routes';
	import { cn } from '$lib/utils.js';

	type Props = {
		routes: Route[];
	};

	let { routes }: Props = $props();
</script>

<div class="flex w-full flex-col gap-4 py-2 text-primary">
	<nav class="grid gap-1 px-2">
		{#if routes}
			{#each routes as route}
				<Button href={route.href} variant={route.variant} size="sm" class="justify-start">
					<svelte:component
						this={route.icon}
						class="mr-6 size-4 min-w-4"
						aria-hidden="true"
					/>
					{route.title}
					{#if route.label}
						<span
							class={cn('ml-auto', {
								'text-background-on': route.variant === 'default',
							})}
						>
							{route.label}
						</span>
					{/if}
				</Button>
			{/each}
		{/if}
	</nav>
</div>
