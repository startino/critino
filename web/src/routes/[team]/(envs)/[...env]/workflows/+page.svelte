<script lang="ts">
	import { goto } from '$app/navigation';
	import * as Dialog from '$lib/components/ui/dialog';
	import * as Form from '$lib/components/ui/form';
	import { EntityControlGrid } from '$lib/components/ui/entity-control-grid';
	import { Typography } from '$lib/components/ui/typography';
	import { type Tables } from '$lib/supabase';
	import { superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { environmentSchema } from '$lib/schema.js';
	import { toast } from 'svelte-sonner';
	import { sluggify } from '$lib/utils.js';

	export let data;

	$: ({ environment, workflows } = data);

	$: createOpen = false;

	const form = superForm(data.form.workflow, {
		validators: zodClient(environmentSchema),
		onSubmit: () => {},
		onUpdated: async ({ form: f }) => {
			if (!f.valid) {
				toast.error('Please fix the errors in the form.');
			}
		},
		onResult: async (event) => {
			if (event.result.type !== 'success') return;

			createOpen = false;

			toast.success(`Created ${$formData.name}`);
		},
	});

	const { form: formData, enhance } = form;
</script>

<Typography class="p-4 text-left" variant="headline-lg">
	{environment.name.split('/').pop()}'s workflows
</Typography>

<EntityControlGrid
	on:click={async ({ detail: workflow }: CustomEvent<Tables<'environments'>>) => {
		await goto(sluggify(`workflows/${workflow.name}`), {
			replaceState: true,
			invalidateAll: true,
		});
	}}
	on:create={async () => {
		createOpen = true;
	}}
	name="workflow"
	entities={workflows}
/>

<!-- <Dialog.Root bind:open={createOpen}> -->
<!-- 	<Dialog.Trigger /> -->
<!-- 	<Dialog.Content class="max-w-2xl"> -->
<!-- 		<Dialog.Header> -->
<!-- 			<Dialog.Title>Creating Environment</Dialog.Title> -->
<!-- 		</Dialog.Header> -->
<!-- 		<form action={`/${team.name}`} method="POST" class="flex flex-col gap-6" use:enhance> -->
<!-- 			<Form.Field {form} name="name"> -->
<!-- 				<Form.Control let:attrs> -->
<!-- 					<Form.Label>Name</Form.Label> -->
<!-- 					<Input {...attrs} bind:value={$formData.name} /> -->
<!-- 				</Form.Control> -->
<!-- 				<Form.FieldErrors /> -->
<!-- 			</Form.Field> -->
<!-- 			<Form.Field {form} name="description"> -->
<!-- 				<Form.Control let:attrs> -->
<!-- 					<Form.Label>Description</Form.Label> -->
<!-- 					<Input {...attrs} bind:value={$formData.description} /> -->
<!-- 				</Form.Control> -->
<!-- 				<Form.FieldErrors /> -->
<!-- 			</Form.Field> -->
<!-- 			<div class="flex w-full flex-col gap-2"> -->
<!-- 				<Button class="mr-auto" on:click={genKey}>Generate Access Key</Button> -->
<!---->
<!-- 				{#if key} -->
<!-- 					<div class="flex items-center justify-start gap-1"> -->
<!-- 						<Typography variant="title-sm">Key:</Typography> -->
<!-- 						<Typography variant="body-sm" class="pt-1 text-left"> -->
<!-- 							{key} -->
<!-- 						</Typography> -->
<!-- 					</div> -->
<!-- 					<Typography class="text-left text-destructive"> -->
<!-- 						Save this access key. -->
<!-- 					</Typography> -->
<!-- 				{/if} -->
<!-- 			</div> -->
<!-- 			<Form.Button>Submit</Form.Button> -->
<!-- 		</form> -->
<!-- 	</Dialog.Content> -->
<!-- </Dialog.Root> -->
