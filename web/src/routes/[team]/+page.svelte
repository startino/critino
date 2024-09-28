<script lang="ts">
	import { EntityControlGrid } from '$lib/components/ui/entity-control-grid';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import type { Tables } from '$lib/supabase';
	import { Button } from '$lib/components/ui/button';

	export let data;

	let { team, environments } = data;

	let createOpen = false;
	let deleteEnvironment: string = '';
</script>

<Breadcrumb crumbs={[{ name: team.name }]} />

<EntityControlGrid
	on:click={async (e) => {}}
	on:create={async () => {
		createOpen = true;
	}}
	on:delete={async (e) => {}}
	entities={environments}
/>

<Dialog.Root bind:open={createOpen}>
	<Dialog.Trigger />
	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title>Creating Environment</Dialog.Title>
		</Dialog.Header>
	</Dialog.Content>
</Dialog.Root>
