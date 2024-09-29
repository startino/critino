<script lang="ts">
	import { TipTap } from '$lib/components/ui/tiptap';
	import { superForm } from 'sveltekit-superforms';
	import * as Form from '$lib/components/ui/form';
	import * as Card from '$lib/components/ui/card';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { critiqueSchema } from '$lib/schema';
	import { toast } from 'svelte-sonner';
	import { Typography } from '$lib/components/ui/typography';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import * as xml from '$lib/xml';
	import { ScrollArea } from '$lib/components/ui/scroll-area';

	export let data;
	let { supabase, forms, team, environment, workflow, agent, critique } = data;

	const form = superForm(forms.critique, {
		dataType: 'json',
		validators: zodClient(critiqueSchema),
		async onSubmit() {
			$formData.id = critique.id;
			$formData.workflow_name = critique.workflow_name;
			$formData.agent_name = critique.agent_name;
			$formData.environment_name = critique.environment_name;
			$formData.team_name = critique.team_name;
			$formData.tags = critique.tags;
			$formData.response = critique.response;
			$formData.optimal = critique.optimal;

			$formData.context = critique.context as Context[];
			$formData.critique = critique.critique;

			const { data: savedCritique, error: eCritique } = await supabase
				.from('critiques')
				.update($formData)
				.eq('id', $formData.id)
				.select('*')
				.single();

			if (!savedCritique || eCritique) {
				toast.error('Error saving critique.');
				return;
			}

			critique = savedCritique;
			toast('Saving critique...');
		},
		onResult() {
			toast('Critique Saved!');
		},
		onError() {
			toast.error('Error saving critique.');
		},
	});

	const { form: formData, enhance } = form;

	type Context = {
		name: string;
		content: string;
	};

	$: conversation = xml.tryParseXmlEvents(critique.context);
	$: query = xml.tryParseXmlEvent(critique.query);
</script>

<Breadcrumb />

<ScrollArea class="flex h-full w-full">
	<form
		class="mx-auto flex h-screen max-w-prose flex-col items-center justify-center gap-8"
		method="POST"
		action="?/send"
		use:enhance
	>
		<div class="flex flex-col items-center justify-center gap-1 text-primary">
			<Typography as="h1" variant="display-sm">Editing Critique</Typography>
			<Typography class="opacity-70" variant="title-md">
				You are critizing the {agent.name}.
			</Typography>
		</div>

		<Card.Root
			class="mx-auto h-max w-full border-surface-variant/80 bg-primary-container/5 text-left"
		>
			<Card.Header>
				<Card.Title>Context</Card.Title>
				<Card.Description>These are the previous messages that were sent.</Card.Description>
			</Card.Header>
			<Card.Content>
				<div class="flex w-full flex-col gap-2">
					{#if conversation}
						{#each conversation as context, index}
							<div class="flex w-full flex-col">
								<small
									class={`flex ${context.name === 'user' ? 'justify-end pr-1' : 'justify-start pl-1'}`}
								>
									{context.name}
								</small>
								<div
									class={`flex ${context.name === 'user' ? 'ml-16 justify-end' : 'mr-16 justify-start'}`}
								>
									<TipTap
										editable={false}
										class="rounded-lg border border-primary/50 bg-primary-container/10 px-2 py-1 font-medium text-primary dark:brightness-125"
										bind:content={context.content}
									/>
								</div>
							</div>
						{/each}
					{:else}
						<div class="flex justify-end">
							<TipTap
								editable={false}
								class="rounded-lg border border-primary/50 bg-primary-container/10 px-2 py-1 font-medium text-primary dark:brightness-125"
								bind:content={critique.context}
							/>
						</div>
					{/if}
					{#if query}
						<div class="flex w-full flex-col">
							<small
								class={`flex ${query.name === 'user' ? 'justify-end pr-1' : 'justify-start pl-1'}`}
							>
								{query.name}
							</small>
							<div
								class={`flex ${query.name === 'user' ? 'ml-16 justify-end' : 'mr-16 justify-start'}`}
							>
								<TipTap
									editable={false}
									class="rounded-lg border border-primary/50 bg-primary-container/10 px-2 py-1 font-medium text-primary dark:brightness-125"
									bind:content={query.content}
								/>
							</div>
						</div>
					{:else}
						<div class="flexml-16 justify-end">
							<TipTap
								editable={false}
								class="rounded-lg border border-primary/50 bg-primary-container/10 px-2 py-1 font-medium text-primary brightness-125"
								bind:content={critique.query}
							/>
						</div>
					{/if}
				</div>

				<hr class="my-8 border-primary/50" />

				<Typography variant="title-md" align="left" class="mr-auto text-primary">
					Agent's Response
				</Typography>

				<Typography
					variant="title-sm"
					align="left"
					class="min-w-none mr-auto pb-2 text-primary/70"
				>
					This is the response that you're critiqueing.
				</Typography>

				<div class="flex justify-start">
					<TipTap
						class="rounded-lg border border-primary/50 bg-primary-container/10 px-2 py-1 text-primary brightness-125"
						bind:content={critique.response}
					></TipTap>
				</div>

				<Typography variant="title-md" align="left" class="mr-auto pt-4 text-secondary">
					Optimal Response
				</Typography>
				<Typography variant="title-sm" align="left" class="mr-auto pb-2 text-secondary/70">
					This is the optimal response, what the response should've been.
					<br />
					(can be the same if the agents answer was good)
				</Typography>

				<div class="flex justify-start">
					<TipTap
						class="rounded-lg border border-secondary/50 bg-secondary-container/10 px-2 py-1 text-secondary brightness-125"
						bind:content={critique.optimal}
					></TipTap>
				</div>
			</Card.Content>
		</Card.Root>

		<Form.Button type="submit" class="w-full">Save</Form.Button>
	</form>
</ScrollArea>
