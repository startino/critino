<script lang="ts">
	import * as Select from '$lib/components/ui/select';
	import type { Team } from './teams';
	import { cn } from '$lib/utils.js';
	import { Typography } from '$lib/components/ui/typography';

	export let isCollapsed: boolean;
	export let teams: Team[];

	$: teams = teams.sort((a, b) => a.label.localeCompare(b.label));

	let selectedTeam = teams.sort((a, b) => a.label.localeCompare(b.label))[0];
</script>

{#if selectedTeam}
	<Select.Root
		portal={null}
		selected={{ value: selectedTeam.label, label: selectedTeam.label }}
		onSelectedChange={(e) => {
			selectedTeam = teams.find((team) => team.label === e?.value) || teams[0];
		}}
	>
		<Select.Trigger
			class={cn(
				'flex items-center gap-2 [&>span]:line-clamp-1 [&>span]:flex [&>span]:w-full [&>span]:items-center [&>span]:gap-1 [&>span]:truncate [&_svg]:h-4 [&_svg]:w-4 [&_svg]:shrink-0',
				isCollapsed &&
					'flex h-9 w-9 shrink-0 items-center justify-center p-0 [&>div>svg]:hidden [&>span]:w-auto'
			)}
			aria-label="Select team"
		>
			<span class="pointer-events-none">
				<svelte:component this={selectedTeam.icon} class={cn(isCollapsed ? 'ml-2' : '')} />
				<span class={cn(isCollapsed ? '!ml-0 !hidden' : 'ml-2')}>
					<Typography variant="title-sm">{selectedTeam.label}</Typography>
				</span>
			</span>
		</Select.Trigger>
		<Select.Content sameWidth={!isCollapsed} align={isCollapsed ? 'start' : undefined}>
			<Select.Group>
				{#each teams as team}
					<Select.Item value={team.label} label={team.label}>
						<div
							class="flex items-center gap-3 [&_svg]:h-4 [&_svg]:w-4 [&_svg]:shrink-0 [&_svg]:text-foreground"
						>
							<svelte:component
								this={team.icon}
								aria-hidden="true"
								class="size-6 shrink-0 text-foreground"
							/>
							<Typography variant="title-sm">{team.label}</Typography>
						</div>
					</Select.Item>
				{/each}
			</Select.Group>
		</Select.Content>
		<Select.Input hidden name="team" />
	</Select.Root>
{:else}
	<p>No teams found</p>
{/if}
