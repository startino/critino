<script lang="ts">
	import * as Tabs from '$lib/components/ui/tabs';
	import CritiqueTable from './critique-table.svelte';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import { Typography } from '$lib/components/ui/typography';
	export let data;

	let { supabase, team, environment, workflow, agents, critiques } = data;
</script>

<Breadcrumb
	crumbs={[
		{ name: team.name, href: `/${team.name}` },
		{ name: 'environments', href: `/${team.name}/environments` },
		{ name: environment.name, href: `/${team.name}/environments/${environment.name}` },
		{ name: 'workflows', href: `/${team.name}/environments/${environment.name}/workflows` },
		{
			name: workflow.name,
			href: `/${team.name}/environments/${environment.name}/workflows/${workflow.name}`,
		},
		{ name: 'critiques' },
	]}
/>

<div class="flex w-full items-center justify-center p-12">
	{#if agents.length > 1}
		<Tabs.Root
			value={(agents.find((agent) => agent.name) ?? { name: '' }).name}
			class="h-full w-full"
		>
			<Tabs.List class="flex w-full gap-2">
				{#each agents as agent}
					<Tabs.Trigger class="flex-1" value={agent.name}>{agent.name}</Tabs.Trigger>
				{/each}
			</Tabs.List>
			{#each agents as agent}
				<Tabs.Content value={agent.name}>
					<CritiqueTable agent={agent.name} {supabase} {environment} {workflow} {critiques} />
				</Tabs.Content>
			{/each}
		</Tabs.Root>
	{:else if agents[0]}
		<CritiqueTable agent={agents[0].name} {supabase} {environment} {workflow} {critiques} />
	{:else}
		<div class="mx-auto h-full w-full text-left">
			<Typography variant="display-lg">No Critiques Created Yet</Typography>
		</div>
	{/if}
</div>
