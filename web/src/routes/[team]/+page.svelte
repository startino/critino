<script lang="ts">
	import { Separator } from '$lib/components/ui/separator';
	import * as Card from '$lib/components/ui/card';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import { goto } from '$app/navigation';
	import { ChevronRight, Plus } from 'lucide-svelte';
	import { TipTap } from '$lib/components/ui/tiptap';

	export let data;

	let { team, environments } = data;
</script>

<Breadcrumb crumbs={[{ name: team.name, href: `/${team.name}` }, { name: 'environments' }]} />

<div>
	<div
		class="grid h-fit w-full grid-cols-1 items-start justify-center gap-4 p-4 sm:grid-cols-1 md:grid-cols-1 lg:grid-cols-2 xl:grid-cols-3"
	>
		{#each environments as environment}
			<button class="h-full" on:click={() => goto(`environments/${environment.name}`)}>
				<Card.Root class="group h-full w-full text-left">
					<Card.Header class="relative gap-2">
						<Card.Title>{environment.name}</Card.Title>
						<Card.Description>
							<TipTap
								class="text-background-on"
								editable={false}
								content={environment.description}
							></TipTap>
						</Card.Description>
						<ChevronRight
							class="transition-100 absolute right-5 top-5 opacity-50 group-hover:opacity-100"
						/>
					</Card.Header>
				</Card.Root>
			</button>
		{/each}

		<button disabled class="h-full opacity-50">
			<Card.Root class="group h-full w-full text-left">
				<Card.Header class="relative">
					<div class="flex h-full w-full flex-col items-center justify-center">
						<Card.Title>Create new Environment</Card.Title>
						<Plus class="size-12" />
					</div>
				</Card.Header>
			</Card.Root>
		</button>
	</div>
</div>
