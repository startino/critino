<script lang="ts">
	import * as Tabs from '$lib/components/ui/tabs';
	import CritiqueTable from './critique-table.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	export let data;

	let { supabase, team, project, workflow, agents, critiques } = data;
</script>

<Breadcrumb
	crumbs={[
		{ name: team.name, href: `/${team.name}` },
		{ name: 'projects', href: `/${team.name}/projects` },
		{ name: project.name, href: `/${team.name}/projects/${project.name}` },
		{ name: 'workflows', href: `/${team.name}/projects/${project.name}/workflows` },
		{
			name: workflow.name,
			href: `/${team.name}/projects/${project.name}/workflows/${workflow.name}`,
		},
		{ name: 'critiques' },
	]}
/>

<div class="flex w-full items-center justify-center p-12">
	{#if agents.length < 1}
		<Tabs.Root value="account" class="w-[400px]">
			<Tabs.List class="grid w-full grid-cols-2">
				{#each agents as agent}
					<Tabs.Trigger value={agent.name}>{agent.name}</Tabs.Trigger>
				{/each}
			</Tabs.List>
			{#each agents as agent}
				<Tabs.Content value={agent.name}>
					<CritiqueTable {supabase} {project} {workflow} {critiques} />
				</Tabs.Content>
			{/each}
		</Tabs.Root>
	{:else}
		<CritiqueTable {supabase} {project} {workflow} {critiques} />
	{/if}
</div>
