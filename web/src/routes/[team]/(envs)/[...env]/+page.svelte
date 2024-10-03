<script lang="ts">
	import { EntityControlGrid } from '$lib/components/ui/entity-control-grid';
	import * as Dialog from '$lib/components/ui/dialog';
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
	import { v4 as uuidv4 } from 'uuid';
	import { sha256 } from 'js-sha256';
	import { sluggify } from '$lib/utils';

	export let data;

	$: ({ supabase, team, environment, environments: allEnvironments } = data);

	$: environments = allEnvironments.filter((env) => env.parent_name === environment.name);

	$: createOpen = false;

	const form = superForm(data.form.environment, {
		validators: zodClient(environmentSchema),
		onSubmit: () => {
			$formData.parent_name = environment.name;
		},
		onUpdated: async ({ form: f }) => {
			if (!f.valid) {
				toast.error('Please fix the errors in the form.');
			}
		},
		onResult: async (event) => {
			if (event.result.type !== 'success') return;

			const encryptedKey = key ? sha256.update(key).hex() : null;

			const { error: eEnvironment } = await supabase.from('environments').insert({
				name: $formData.parent_name + '/' + $formData.name,
				parent_name: $formData.parent_name,
				team_name: team.name,
				description: $formData.description,
				key: encryptedKey,
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
				{
					name: $formData.parent_name + '/' + $formData.name,
					parent_name: $formData.parent_name,
					team_name: team.name,
					description: $formData.description,
					key: encryptedKey,
					created_at: new Date().toISOString(),
				},
			];

			createOpen = false;

			toast.success(`Created ${$formData.name}`);
		},
	});

	const { form: formData, enhance } = form;

	let key: string | null = null;

	const genKey = () => {
		key =
			'sp-critino-env-' +
			sha256.update(uuidv4().replace('-', '') + uuidv4().replace('-', '')).hex();
	};
</script>

<Typography class="p-4 text-left" variant="headline-lg">
	{environment.name.split('/').pop()}'s environments
</Typography>

<EntityControlGrid
	on:click={async ({ detail: env }: CustomEvent<Tables<'environments'>>) => {
		await goto(sluggify(`${env.parent_name!.split('/').pop()}/${env.name}`), {
			replaceState: true,
			invalidateAll: true,
		});
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
	entities={environments.map((env) => ({
		...env,
		name: env.name.split('/').pop() ?? 'failed to get env name',
	}))}
/>

<Dialog.Root bind:open={createOpen}>
	<Dialog.Trigger />
	<Dialog.Content class="max-w-2xl">
		<Dialog.Header>
			<Dialog.Title>Creating Environment</Dialog.Title>
		</Dialog.Header>
		<form action={`/${team.name}`} method="POST" class="flex flex-col gap-6" use:enhance>
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
			<div class="flex w-full flex-col gap-2">
				<Button class="mr-auto" on:click={genKey}>Generate Access Key</Button>

				{#if key}
					<div class="flex items-center justify-start gap-1">
						<Typography variant="title-sm">Key:</Typography>
						<Typography variant="body-sm" class="pt-1 text-left">
							{key}
						</Typography>
					</div>
					<Typography class="text-left text-destructive">
						Save this access key.
					</Typography>
				{/if}
			</div>
			<Form.Button>Submit</Form.Button>
		</form>
	</Dialog.Content>
</Dialog.Root>
