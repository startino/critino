<script lang="ts">
	import { goto } from '$app/navigation';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import * as Card from '$lib/components/ui/card';
	import { Separator } from '$lib/components/ui/separator';
	import { ChevronRight, Plus } from 'lucide-svelte';
	export let data;

	let { team, project, agents } = data;
</script>

<Breadcrumb
	crumbs={[
		{ name: team.name, href: '/' },
		{ name: 'projects', href: '/projects' },
		{ name: project.name, href: '/projects/' + project.name },
		{ name: 'agents' },
	]}
/>

<div class="flex w-full flex-col items-center justify-start">
	<div
		class="mx-auto grid h-fit w-full grid-cols-1 items-start justify-center gap-4 p-4 sm:grid-cols-1 md:grid-cols-1 lg:grid-cols-2 xl:grid-cols-3"
	>
		{#each agents as agent}
			<button disabled class="group h-full disabled:opacity-50">
				<Card.Root class="h-full w-full text-left">
					<Card.Header class="relative">
						<Card.Title>{agent.name}</Card.Title>
						<Card.Description>{agent.description}</Card.Description>
						<ChevronRight class="transition-100 absolute right-5 top-5 opacity-50" />
					</Card.Header>
				</Card.Root>
			</button>
		{/each}
		<button disabled class="h-full opacity-50" on:click={() => goto(`${project.name}`)}>
			<Card.Root class="group h-full w-full text-left">
				<Card.Header class="relative">
					<div class="flex h-full w-full flex-col items-center justify-center">
						<Card.Title>Create new Agent</Card.Title>
						<Plus class="size-12" />
					</div>
				</Card.Header>
			</Card.Root>
		</button>
	</div>
</div>
