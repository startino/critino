<script lang="ts">
	import Nav from '$lib/components/ui/nav.svelte';
	import { Separator } from '$lib/components/ui/separator';
	import { Typography } from '$lib/components/ui/typography';
	import { primaryRoutes } from './routes';

	export let data;
	let { team, environment, workflow, agents, critiques } = data;
</script>

<Breadcrumb />
<div class="flex h-full w-full">
	<div class="relative flex w-full flex-col overflow-hidden text-nowrap">
		<slot />
	</div>
</div>
