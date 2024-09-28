<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { ChevronRight, Plus, X } from 'lucide-svelte';
	import { TipTap } from '$lib/components/ui/tiptap';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	export let name: string = '';
	export let entities: { name: string; description: string }[];
</script>

<div>
	<div
		class="grid h-fit w-full grid-cols-1 items-start justify-center gap-4 p-4 sm:grid-cols-1 md:grid-cols-1 lg:grid-cols-2 xl:grid-cols-3"
	>
		{#each entities as entity}
			<button class="h-full" on:click={() => dispatch(`click`, entity)}>
				<Card.Root
					class="duration-400 group h-full w-full text-left transition-all ease-in-out hover:scale-[102%] hover:shadow-lg"
				>
					<Card.Header class="relative min-h-28 gap-2 space-y-0">
						<Card.Title>{entity.name}</Card.Title>
						<Card.Description>
							<TipTap
								class="text-background-on"
								editable={false}
								content={entity.description}
							></TipTap>
						</Card.Description>
						<ChevronRight
							class="duration-400 absolute right-5 top-5 opacity-50 transition-all ease-in-out group-hover:scale-150 group-hover:opacity-100"
						/>

						<div
							role="button"
							tabindex="0"
							class="duration-400 absolute bottom-5 right-5 scale-100 cursor-pointer text-error opacity-60 transition-all ease-in-out hover:scale-150 hover:opacity-100"
							on:click={(event) => {
								event.stopPropagation();
								dispatch('delete');
							}}
							on:keydown={(event) => {
								if (event.key === 'Enter' || event.key === ' ') {
									event.preventDefault();
									event.stopPropagation();
									dispatch('delete');
								}
							}}
						>
							<X
								class="scale-0 opacity-0 group-hover:scale-100 group-hover:opacity-100"
							/>
						</div>
					</Card.Header>
				</Card.Root>
			</button>
		{/each}

		<button class="h-full" on:click={() => dispatch(`create`)}>
			<Card.Root
				class="duration-400 group h-full w-full text-left transition-all ease-in-out hover:scale-[102%] hover:shadow-lg"
			>
				<Card.Header class="relative h-full min-h-28 gap-2 space-y-0">
					<div class="flex h-full w-full flex-col items-center justify-center">
						{#if name}
							<Card.Title>create new {name}</Card.Title>
						{/if}
						<Plus
							class="duration-400 size-12 opacity-100 transition-all ease-in-out group-hover:scale-150 group-hover:opacity-100"
						/>
					</div>
				</Card.Header>
			</Card.Root>
		</button>
	</div>
</div>
