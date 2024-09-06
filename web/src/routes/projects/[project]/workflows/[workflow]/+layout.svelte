<script lang="ts">
	import Nav from '$lib/components/ui/nav.svelte';
	import { Separator } from '$lib/components/ui/separator';
	import { Typography } from '$lib/components/ui/typography';
	import { primaryRoutes } from './routes';

	export let data;
	let { team, project, workflow, agents, critiques } = data;
</script>

<div class="flex h-full w-full">
	<!-- Nav -->
	<div class="flex h-full w-64 flex-col items-start justify-start">
		<div class="flex h-14 w-full items-center justify-start px-4">
			<Typography variant="title-md" class="mb-0 pb-0">Project {project.name}</Typography>
		</div>
		<Separator class="mt-0 pt-0 opacity-20" />

		<Nav routes={primaryRoutes(project, workflow, agents, critiques)} />
	</div>
	<!-- /Nav -->

	<Separator orientation="vertical" class="ml-0 pl-0 opacity-20" />

	<div class="relative flex w-full flex-col overflow-hidden text-nowrap">
		<slot />
	</div>
</div>
