<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { cn } from '$lib/utils.js';
	import type { Route } from './routes';

	export let isCollapsed: boolean;
	export let routes: Route[];
</script>

<div class="flex flex-col gap-4 py-2 text-primary">
	<nav class="grid gap-1 px-2">
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
	</nav>
</div>
