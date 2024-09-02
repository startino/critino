<script lang="ts">
	import * as Resizable from '$lib/components/ui/resizable';
	import { Separator } from '$lib/components/ui/select';
	import { Typography } from '$lib/components/ui/typography';
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { goto } from '$app/navigation';

	export let data;

	let { team, projects } = data;
</script>

<Resizable.Pane>
	<div class="flex h-14 items-center px-4">
		<Typography as="h1" variant="body-lg" class="flex items-center justify-center">
			{team.name}
			<span class="px-4 text-2xl opacity-30">/</span>
			projects
		</Typography>
	</div>
	<Separator />
	<div
		class="mx-auto grid h-full w-full grid-cols-1 items-start justify-center gap-4 p-4 sm:grid-cols-1 md:grid-cols-1 lg:grid-cols-2 xl:grid-cols-3"
	>
		{#each projects as project}
			<button on:click={() => goto(`projects/${project.id}`)}>
				<Card.Root class="hover:cursor-pointer">
					<Card.Header>
						<Card.Title>{project.name}</Card.Title>
						<Card.Description>{project.description}</Card.Description>
					</Card.Header>
				</Card.Root>
			</button>
		{/each}
	</div>
</Resizable.Pane>
