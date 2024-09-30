<script lang="ts">
	import { EntityControlGrid } from '$lib/components/ui/entity-control-grid';
	import { Typography } from '$lib/components/ui/typography';

	export let data;

	$: ({ params, workflows } = data);
</script>

<Typography class="p-4 text-left" variant="headline-lg">
	{params.env?.toString().split('/').pop()}'s workflows
</Typography>

<EntityControlGrid name="workflow" entities={workflows} />
