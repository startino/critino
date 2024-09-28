<script lang="ts">
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import { EntityControlGrid } from '$lib/components/ui/entity-control-grid';

	export let data;

	let { team, environments } = data;
</script>

<Breadcrumb crumbs={[{ name: team.name }]} />

<EntityControlGrid entities={environments} />
