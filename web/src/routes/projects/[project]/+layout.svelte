<script lang="ts">
	import Nav from '$lib/components/ui/nav.svelte';
	import { Separator } from '$lib/components/ui/separator';
	import { Typography } from '$lib/components/ui/typography';
	import { primaryRoutes } from './routes';

	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import * as Card from '$lib/components/ui/card';
	import { ChevronRight } from 'lucide-svelte';
	import { goto } from '$app/navigation';
	import { Plus } from 'lucide-svelte';

	export let data;
	let { team, project, agents } = data;
</script>

<div class="flex h-full w-full">
	<!-- Nav -->
	<div class="flex h-full w-64 flex-col items-start justify-start">
		<div class="flex h-14 w-full items-center justify-start px-4">
			<Typography variant="title-md" class="mb-0 pb-0">Project {project.name}</Typography>
		</div>
		<Separator class="mt-0 pt-0 opacity-40" />

		<Nav routes={primaryRoutes(project)} />
	</div>
	<!-- /Nav -->

	<Separator orientation="vertical" class="ml-0 pl-0" />

	<div class="relative flex w-full flex-col overflow-hidden text-nowrap">
		<slot />
		<!---->
		<!-- 	<Separator class="mt-0 pt-0 opacity-40" /> -->
		<!-- 	<div class="flex h-full w-full flex-col"> -->
		<!---->
		<!-- 		<div class="flex h-full w-full flex-col items-center justify-center"> -->
		<!-- 			<Typography as="h2" variant="headline-sm">API Endpoints:</Typography> -->
		<!-- 			<Typography as="p" variant="body-md"> -->
		<!-- 				GET /projects/{project.name} -->
		<!-- 			</Typography> -->
		<!-- 		</div> -->
		<!-- 	</div> -->
	</div>
</div>
