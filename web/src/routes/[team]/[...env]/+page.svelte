<script lang="ts">
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import { EntityControlGrid } from '$lib/components/ui/entity-control-grid';

	export let data;

	let { team, params } = data;
</script>

<Breadcrumb crumbs={[{ name: team.name, href: `/${team.name}` }, { name: 'environments' }]} />

<EntityControlGrid entities={[]} />
