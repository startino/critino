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

	export let data;

	let { supabase, params, team, environments: allEnvironments } = data;

	let environments = allEnvironments.filter((env) => env.name.includes('/'));

	let createOpen = false;

	const form = superForm(data.form.environment, {
		validators: zodClient(environmentSchema),
		onUpdated: ({ form: f }) => {
			if (!f.valid) {
				toast.error('Please fix the errors in the form.');
			}
		},
		onResult: async (event) => {
			if (event.result.type !== 'success') return;

			environments = [...environments, $formData];
			createOpen = false;

			toast.success(`Created ${$formData.name}`);
		},
	});

	$: {
		$formData.name = $formData.name;
		$formData.description = $formData.description;
		$formData.full_name = params.env + '/' + $formData.name;
		$formData.parent_name = params.env;

		console.log(`form data: ${JSON.stringify($formData, null, 2)}`);
	}

	const { form: formData, enhance } = form;
</script>

<Breadcrumb crumbs={[{ name: team.name }]} />

<EntityControlGrid
	on:click={({ detail: env }: CustomEvent<Tables<'environments'>>) => {
		console.log(env.name);
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
	entities={environments}
/>

<Dialog.Root bind:open={createOpen}>
	<Dialog.Trigger />
	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title>Creating Environment</Dialog.Title>
			<Dialog.Description>Creating Environment</Dialog.Description>
		</Dialog.Header>
		<form action={`/${team.name}`} method="POST" class="w-2/3 space-y-6" use:enhance>
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
