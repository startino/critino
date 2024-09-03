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
	<div class="w-64">
		<div
			class="flex h-full w-full flex-col items-start justify-start overflow-hidden text-nowrap"
		>
			<div class="flex h-14 w-full items-center justify-start px-4">
				<Typography variant="title-lg" class="mb-0 pb-0">Table Editor</Typography>
			</div>
			<Separator class="mt-0 pt-0 opacity-40" />

			<Nav routes={primaryRoutes(project)} />
		</div>
	</div>
	<!-- /Nav -->

	<Separator orientation="vertical" class="ml-0 pl-0" />
	<div class="flex h-full w-full flex-col items-center justify-center">
		<slot />
		<!-- 	<div class="flex h-14 w-full items-center justify-start px-4"> -->
		<!-- 		<Breadcrumb -->
		<!-- 			crumbs={[ -->
		<!-- 				{ name: team.name, href: '/' }, -->
		<!-- 				{ name: 'projects', href: '/projects' }, -->
		<!-- 				{ name: project.name }, -->
		<!-- 			]} -->
		<!-- 		/> -->
		<!-- 	</div> -->
		<!---->
		<!-- 	<Separator class="mt-0 pt-0 opacity-40" /> -->
		<!-- 	<div class="flex h-full w-full flex-col"> -->
		<!-- 		<div class="flex h-full w-full flex-col items-center justify-center"> -->
		<!-- 			<Typography as="h2" variant="headline-sm">Agents</Typography> -->
		<!---->
		<!-- 			<div -->
		<!-- 				class="mx-auto grid h-fit w-full grid-cols-1 items-start justify-center gap-4 p-4 sm:grid-cols-1 md:grid-cols-1 lg:grid-cols-2 xl:grid-cols-3" -->
		<!-- 			> -->
		<!-- 				{#each agents as agent} -->
		<!-- 					<button -->
		<!-- 						class="h-full" -->
		<!-- 						on:click={() => goto(`projects/${project.name}/${agent.name}`)} -->
		<!-- 					> -->
		<!-- 						<Card.Root class="group h-full w-full text-left hover:cursor-pointer"> -->
		<!-- 							<Card.Header class="relative"> -->
		<!-- 								<Card.Title>{agent.name}</Card.Title> -->
		<!-- 								<Card.Description>{agent.description}</Card.Description> -->
		<!-- 								<ChevronRight -->
		<!-- 									class="transition-100 absolute right-5 top-5 opacity-50 group-hover:opacity-100" -->
		<!-- 								/> -->
		<!-- 							</Card.Header> -->
		<!-- 						</Card.Root> -->
		<!-- 					</button> -->
		<!-- 				{/each} -->
		<!-- 				<button class="h-full" on:click={() => goto(`${project.name}`)}> -->
		<!-- 					<Card.Root class="group h-full w-full text-left hover:cursor-pointer"> -->
		<!-- 						<Card.Header class="relative"> -->
		<!-- 							<div -->
		<!-- 								class="flex h-full w-full flex-col items-center justify-center" -->
		<!-- 							> -->
		<!-- 								<Card.Title>Create new Agent</Card.Title> -->
		<!-- 								<Plus class="size-12" /> -->
		<!-- 							</div> -->
		<!-- 						</Card.Header> -->
		<!-- 					</Card.Root> -->
		<!-- 				</button> -->
		<!-- 			</div> -->
		<!-- 		</div> -->
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
