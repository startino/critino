<script lang="ts">
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import CritiqueTable from './critique-table.svelte';
	import * as Card from '$lib/components/ui/card';
	export let data;

	let { supabase, team, project, workflow, agents, critiques } = data;
</script>

<Breadcrumb
	crumbs={[
		{ name: team.name, href: '/' },
		{ name: 'projects', href: '/projects' },
		{ name: project.name, href: `/projects/${project.name}` },
		{ name: 'workflows', href: `/projects/${project.name}/workflows` },
		{ name: workflow.name, href: `/projects/${project.name}/workflows/${workflow.name}` },
		{ name: 'critiques' },
	]}
/>

<div class="flex w-full items-center justify-center p-12">
	<Card.Root class="mx-auto h-full w-full border-surface-variant/80 bg-primary/5 text-left">
		<Card.Header class="border-b border-surface-variant/80">
			<Card.Title>Critiques</Card.Title>
		</Card.Header>
		<Card.Content class="p-0">
			<CritiqueTable {supabase} {project} {workflow} {critiques} />
		</Card.Content>
	</Card.Root>
</div>
