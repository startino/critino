<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import { goto } from '$app/navigation';
	import { ChevronRight, Plus } from 'lucide-svelte';
	import { EntityControlGrid } from '$lib/components/ui/entity-control-grid';
	import { Typography } from '$lib/components/ui/typography';

	export let data;

	$: ({ params, workflows } = data);
</script>

<Typography class="p-4" align="left" variant="headline-lg">
	{params.env?.toString().split('/').pop()}'s workflows
</Typography>

<EntityControlGrid name="workflow" entities={workflows} />
