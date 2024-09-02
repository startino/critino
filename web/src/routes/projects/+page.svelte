<script lang="ts">
	import { Separator } from '$lib/components/ui/separator';
	import * as Card from '$lib/components/ui/card';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import { goto } from '$app/navigation';
	import { ChevronRight } from 'lucide-svelte';

	export let data;

	let { team, projects } = data;
</script>

<div class="w-full">
	<div class="flex h-14 items-center px-4">
		<Breadcrumb crumbs={[{ name: team.name, href: '/' }, { name: 'projects' }]} />
	</div>
	<Separator class="mt-0 pt-0" />
	<div
		class="mx-auto grid h-full w-full grid-cols-1 items-start justify-center gap-4 p-4 sm:grid-cols-1 md:grid-cols-1 lg:grid-cols-2 xl:grid-cols-3"
	>
		{#each projects as project}
			<button on:click={() => goto(`projects/${project.id}`)}>
				<Card.Root class="group text-left hover:cursor-pointer">
					<Card.Header class="relative">
						<Card.Title>{project.name}</Card.Title>
						<Card.Description>{project.description}</Card.Description>
						<ChevronRight
							class="transition-100 absolute right-5 top-5 opacity-50 group-hover:opacity-100"
						/>
					</Card.Header>
				</Card.Root>
			</button>
		{/each}
	</div>
</div>
