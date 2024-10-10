<script lang="ts">
	import * as Tabs from '$lib/components/ui/tabs';
	import CritiqueTable from './critique-table.svelte';
	import { Typography } from '$lib/components/ui/typography';
	import type { Tables } from '$lib/supabase';
	export let data;

	$: ({ supabase, team, environment, workflow, agents, critiques } = data);

	const filterAgents = (agents: Tables<'agents'>[]) =>
		agents.filter((agent) => critiques.some((critique) => critique.agent_name === agent.name));
</script>

<div class="flex w-full items-center justify-center p-12">
	{#if filterAgents(agents).length > 1}
		<Tabs.Root
			value={(filterAgents(agents).find((agent) => agent.name) ?? { name: '' }).name}
			class="h-full w-full"
		>
			<Tabs.List class="flex w-full gap-2">
				{#each filterAgents(agents) as agent}
					<Tabs.Trigger class="flex-1" value={agent.name}>{agent.name}</Tabs.Trigger>
				{/each}
			</Tabs.List>
			{#each filterAgents(agents) as agent}
				<Tabs.Content value={agent.name}>
					<CritiqueTable
						agent={agent.name}
						{supabase}
						{environment}
						{workflow}
						{critiques}
					/>
				</Tabs.Content>
			{/each}
		</Tabs.Root>
	{:else if filterAgents(agents)[0]}
		<CritiqueTable
			agent={filterAgents(agents)[0]!.name}
			{supabase}
			{environment}
			{workflow}
			{critiques}
		/>
	{:else}
		<div class="mx-auto h-full w-full text-left">
			<Typography variant="display-lg">No Critiques Created Yet</Typography>
		</div>
	{/if}
</div>
