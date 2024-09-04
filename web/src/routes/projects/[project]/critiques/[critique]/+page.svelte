<script lang="ts">
	import { TipTap } from '$lib/components/ui/tiptap';
	import SuperDebug, { superForm } from 'sveltekit-superforms';
	import * as Form from '$lib/components/ui/form';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { critiqueSchema } from '$lib/schema';
	import { toast } from 'svelte-sonner';
	import { onMount } from 'svelte';
	import { Typography } from '$lib/components/ui/typography/index.js';

	export let data;
	let { forms, agent, critique } = data;

	const form = superForm(forms.critique, {
		dataType: 'json',
		validators: zodClient(critiqueSchema),
	});

	const { form: formData, enhance } = form;

	type Context = {
		name: string;
		content: string;
		index: number;
	};

	onMount(async () => {
		$formData.id = critique.id;
		$formData.agent_name = critique.agent_name;
		$formData.project_name = critique.project_name;
		$formData.team_name = critique.team_name;
		$formData.tags = critique.tags;
		$formData.response = critique.response;
		$formData.optimal = critique.optimal;

		$formData.context = critique.context as Context[];
		$formData.critique = critique.critique;
	});
</script>

<!-- <div class="fixed bottom-5 left-5 opacity-30"> -->
<!-- 	<SuperDebug data={$formData}></SuperDebug> -->
<!-- </div> -->

<form
	class="mx-auto my-auto flex max-w-prose flex-col items-center justify-center gap-8 py-8"
	method="POST"
	use:enhance
	on:submit={() => toast('Submitting critique...')}
>
	<div class="flex flex-col items-center justify-center gap-1 text-primary">
		<Typography as="h1" variant="display-sm">Editing Critique</Typography>
		<Typography class="opacity-70" variant="title-md">
			You are critizing the {agent.name}.
		</Typography>
	</div>

	<div class="flex flex-col rounded-lg border-2 border-primary bg-primary-container/20 p-4">
		<!-- Context -->
		<Typography variant="title-md" align="right" class="ml-auto text-primary">
			Context
		</Typography>
		<Typography variant="title-sm" align="right" class="ml-auto pb-2 text-primary/70">
			These are the previous messages that were sent.
		</Typography>
		<div class="flex w-full flex-col gap-2">
			{#each $formData.context as context, index}
				<div
					class={`flex ${context.name === 'user' ? 'ml-16 justify-end' : 'mr-16 justify-start'}`}
				>
					<TipTap
						class="rounded-lg border border-primary/30 bg-primary-container/10 px-2 py-1 text-primary-container-on"
						bind:content={$formData.context[index]!.content}
					/>
				</div>
			{/each}
		</div>

		<hr class="my-8 border-primary/50" />

		<Typography variant="title-md" align="left" class="mr-auto text-primary">
			Agent's Response
		</Typography>

		<Typography variant="title-sm" align="left" class="min-w-none mr-auto pb-2 text-primary/70">
			This is the response that you're critiqueing.
		</Typography>

		<div class="flex justify-start">
			<TipTap
				class="rounded-lg border border-primary/50 bg-primary-container/10 px-2 py-1 text-primary-container-on"
				bind:content={$formData.response}
			></TipTap>
		</div>

		<Typography variant="title-md" align="left" class="mr-auto pt-4 text-success">
			Optimal Response
		</Typography>
		<Typography variant="title-sm" align="left" class="mr-auto pb-2 text-success/70">
			This is what the response should've been.
		</Typography>

		<div class="flex justify-start">
			<TipTap
				class="rounded-lg border border-success/50 bg-success-container/10 px-2 py-1 text-success-container-on"
				bind:content={$formData.optimal}
			></TipTap>
		</div>
	</div>

	<Form.Button class="w-full">Submit</Form.Button>
</form>
