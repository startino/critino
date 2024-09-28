<script lang="ts">
	import { goto } from '$app/navigation';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import { EntityControlGrid } from '$lib/components/ui/entity-control-grid';

	export let data;

	let { team, environments } = data;
</script>

<Breadcrumb crumbs={[{ name: team.name }]} />

<EntityControlGrid
	on:click={async (e) => {
		await goto(`/${team.name}/${e.detail.name}`);
	}}
	entities={environments}
/>
