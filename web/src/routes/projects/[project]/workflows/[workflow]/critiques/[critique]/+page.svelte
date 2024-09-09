<script lang="ts">
	import { TipTap } from '$lib/components/ui/tiptap';
	import { superForm } from 'sveltekit-superforms';
	import * as Form from '$lib/components/ui/form';
	import * as Card from '$lib/components/ui/card';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { critiqueSchema } from '$lib/schema';
	import { toast } from 'svelte-sonner';
	import { onMount } from 'svelte';
	import { Typography } from '$lib/components/ui/typography';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';

	export let data;
	let { forms, team, project, workflow, agent, critique } = data;

	const form = superForm(forms.critique, {
		dataType: 'json',
		validators: zodClient(critiqueSchema),
		onSubmit() {
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
		index: number;
	};

	onMount(async () => {
		$formData.id = critique.id;
		$formData.workflow_name = critique.workflow_name;
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

<Breadcrumb
	crumbs={[
		{ name: team.name, href: '/' },
		{ name: 'projects', href: '/projects' },
		{ name: project.name, href: `/projects/${project.name}` },
		{ name: 'workflows', href: `/projects/${project.name}/workflows` },
		{ name: workflow.name, href: `/projects/${project.name}/workflows/${workflow.name}` },
		{
			name: 'critiques',
			href: `/projects/${project.name}/workflows/${workflow.name}/critiques`,
		},
		{ name: critique.id },
	]}
/>

<form
	class="mx-auto my-auto flex max-w-prose flex-col items-center justify-center gap-8 py-8"
	method="POST"
	use:enhance
>
	<div class="flex flex-col items-center justify-center gap-1 text-primary">
		<Typography as="h1" variant="display-sm">Editing Critique</Typography>
		<Typography class="opacity-70" variant="title-md">
			You are critizing the {agent.name}.
		</Typography>
	</div>

	<Card.Root
		class="mx-auto h-full w-full border-surface-variant/80 bg-primary-container/5 text-left"
	>
		<Card.Header>
			<Card.Title>Context</Card.Title>
			<Card.Description>These are the previous messages that were sent.</Card.Description>
		</Card.Header>
		<Card.Content>
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

			<Typography
				variant="title-sm"
				align="left"
				class="min-w-none mr-auto pb-2 text-primary/70"
			>
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
		</Card.Content>
	</Card.Root>

	<Form.Button class="w-full">Save</Form.Button>
</form>
