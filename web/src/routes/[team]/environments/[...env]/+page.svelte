<script lang="ts">
	import { EntityControlGrid } from '$lib/components/ui/entity-control-grid';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import type { Tables } from '$lib/supabase';
	import { Input } from '$lib/components/ui/input';
	import * as Form from '$lib/components/ui/form';
	import { superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { toast } from 'svelte-sonner';
	import { environmentSchema } from '$lib/schema';
	import { goto } from '$app/navigation';
	import { Button } from '$lib/components/ui/button';
	import { Typography } from '$lib/components/ui/typography';

	export let data;

	let { supabase, team } = data;

	$: params = data.params;
	$: allEnvironments = data.environments;
	$: environments = allEnvironments.filter((env) => env.name.startsWith(params.env + '/'));

	let createOpen = false;

	const form = superForm(data.form.environment, {
		validators: zodClient(environmentSchema),
		onSubmit: () => {
			$formData.parent_name = params.env;
		},
		onUpdated: async ({ form: f }) => {
			if (!f.valid) {
				toast.error('Please fix the errors in the form.');
			}
		},
		onResult: async (event) => {
			if (event.result.type !== 'success') return;

			const { error: eEnvironment } = await supabase.from('environments').insert({
				name: $formData.parent_name + '/' + $formData.name,
				parent_name: $formData.parent_name,
				team_name: params.team,
				description: $formData.description,
			});

			if (eEnvironment) {
				console.error(
					`Error creating new environment\nError: ${JSON.stringify(eEnvironment, null, 2)}\nForm: ${JSON.stringify(form, null, 2)}`
				);
				toast.error('Error creating new environment');
				return;
			}

			environments = [
				...environments,
				{ ...$formData, name: $formData.parent_name + '/' + $formData.name },
			];

			createOpen = false;

			toast.success(`Created ${$formData.name}`);
		},
	});

	const { form: formData, enhance } = form;
</script>

<Breadcrumb />

<div class="m-5 flex w-full flex-col items-start">
	<Button
		on:click={async () => {
			await goto(`${params.env.split('/').pop()}/workflows`);
		}}
		size="lg"
	>
		Workflows
	</Button>

	<Typography as="h1" variant="headline-lg" class="pt-5">Environments</Typography>
</div>

<EntityControlGrid
	on:click={async ({ detail: env }: CustomEvent<Tables<'environments'>>) => {
		await goto(`${env.parent_name.split('/').pop()}/${env.name}`);
	}}
	on:create={async () => {
		createOpen = true;
	}}
	on:delete={async ({ detail: env }: CustomEvent<Tables<'environments'>>) => {
		await supabase
			.from('environments')
			.delete()
			.eq('name', env.name)
			.eq('team_name', env.team_name);

		environments = environments.filter((e) => e.name !== env.name);

		toast.success(`Deleted ${env.name}`);
	}}
	entities={environments.map((env) => ({ ...env, name: env.name.split('/').pop() }))}
/>

<Dialog.Root bind:open={createOpen}>
	<Dialog.Trigger />
	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title>Creating Environment</Dialog.Title>
			<Dialog.Description>Creating Environment</Dialog.Description>
		</Dialog.Header>
		<form
			action={`/${team.name}/environments`}
			method="POST"
			class="w-2/3 space-y-6"
			use:enhance
		>
			<Form.Field {form} name="name">
				<Form.Control let:attrs>
					<Form.Label>Name</Form.Label>
					<Input {...attrs} bind:value={$formData.name} />
				</Form.Control>
				<Form.FieldErrors />
			</Form.Field>
			<Form.Field {form} name="description">
				<Form.Control let:attrs>
					<Form.Label>Description</Form.Label>
					<Input {...attrs} bind:value={$formData.description} />
				</Form.Control>
				<Form.FieldErrors />
			</Form.Field>
			<Form.Button>Submit</Form.Button>
		</form>
	</Dialog.Content>
</Dialog.Root>
