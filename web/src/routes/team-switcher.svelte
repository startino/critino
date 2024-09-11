<script lang="ts">
	import * as Select from '$lib/components/ui/select';
	import { Typography } from '$lib/components/ui/typography';
	import type { Database, Profile, Team } from '$lib/supabase';
	import { Icon } from '$lib/icons';
	import { ChevronDown } from 'lucide-svelte';
	import type { SupabaseClient, User } from '@supabase/supabase-js';
	import { goto } from '$app/navigation';

	export let user: User & Profile;
	export let supabase: SupabaseClient<Database>;
	export let selectedTeam: Team;
	export let isCollapsed: boolean;
	export let teams: Team[];
</script>

{#if selectedTeam}
	<Select.Root
		portal={null}
		selected={{ value: selectedTeam.name, label: selectedTeam.name }}
		onSelectedChange={async (e) => {
			selectedTeam = teams.find((team) => team.name === e?.value) || teams[0];

			await supabase
				.from('profiles')
				.update({ selected_team: selectedTeam.name })
				.eq('id', user.id);

			window.location.href = '/';
		}}
	>
		<Select.Trigger class="relative grid h-12 border-primary/0" aria-label="Select team">
			<div
				class="absolute bottom-0 left-0 right-0 top-0 ml-0.5 flex items-center justify-start"
			>
				<Icon src={selectedTeam.icon_url} class="mr-3 size-11 min-h-11 min-w-11" />
				<div class="flex w-full items-center justify-between pr-2">
					<Typography variant="title-md">{selectedTeam.name}</Typography>
					<ChevronDown class="text-primary opacity-50" />
				</div>
			</div>
		</Select.Trigger>
		<Select.Content sameWidth={!isCollapsed} align={isCollapsed ? 'center' : undefined}>
			<Select.Group>
				{#each teams as team}
					<Select.Item
						class="flex items-center justify-start gap-2"
						value={team.name}
						label={team.name}
					>
						<Icon
							src={team.icon_url}
							aria-hidden="true"
							class="size-8 min-h-8 min-w-8"
						/>
						<Typography variant="title-sm">{team.name}</Typography>
					</Select.Item>
				{/each}
			</Select.Group>
		</Select.Content>
		<Select.Input hidden name="team" />
	</Select.Root>
{:else}
	<p>No teams found</p>
{/if}
