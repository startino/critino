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
	import { Separator } from '$lib/components/ui/separator/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { Typography } from '$lib/components/ui/typography/index.js';

	export let data;

	let { supabase, params, team, environments: allEnvironments } = data;

	let environments = allEnvironments.filter((env) => !env.name.includes('/'));

	let createOpen = false;

	const form = superForm(data.form.environment, {
		validators: zodClient(environmentSchema),
		onSubmit: () => {
			$formData.parent_name = null;
		},
		onUpdated: async ({ form: f }) => {
			if (!f.valid) {
				toast.error('Please fix the errors in the form.');
			}
		},
		onResult: async (event) => {
			if (event.result.type !== 'success') return;

			const { error: eEnvironment } = await supabase.from('environments').insert({
				name: $formData.name,
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

			environments = [...environments, $formData];
			createOpen = false;

			toast.success(`Created ${$formData.name}`);
		},
	});

	const { form: formData, enhance } = form;
</script>

<Breadcrumb />

<EntityControlGrid
	on:click={async ({ detail: env }: CustomEvent<Tables<'environments'>>) => {
		await goto(`environments/${env.name}`);
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
		<form method="POST" class="w-2/3 space-y-6" use:enhance>
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
