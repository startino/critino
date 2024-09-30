<script lang="ts">
	import { Typography } from '$lib/components/ui/typography';
	import { sha256 } from 'js-sha256';
	import { afterUpdate, onMount } from 'svelte';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Button } from '$lib/components/ui/button';
	import { toast } from 'svelte-sonner';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb/index.js';

	export let data;

	$: ({ team } = data);

	let teamKey = '';

	const persistentAuthTeam = () => {
		if (!team) {
			return false;
		}
		if (!team.key) {
			return true;
		}

		if (sha256.update(localStorage.getItem('key' + team.name) ?? '').hex() !== team.key) {
			return false;
		}
		return true;
	};

	const authenticateTeam = () => {
		if (!team) {
			return false;
		}
		if (!team.key) {
			return true;
		}

		if (sha256.update(teamKey).hex() !== team.key) {
			teamKey = localStorage.getItem('key' + team.name) ?? '';
			if (sha256.update(teamKey).hex() !== team.key) {
				toast.error('Invalid key.');
				return false;
			}
		}

		localStorage.setItem('key' + team.name, teamKey!);
		return true;
	};

	let authenticated = false;
	onMount(() => {
		authenticated = false;
		authenticated = persistentAuthTeam();
	});

	afterUpdate(() => {
		authenticated = false;
		authenticated = persistentAuthTeam();
	});
</script>

{#if !authenticated}
	<div class="relative flex w-full flex-col overflow-hidden text-nowrap">
		<Breadcrumb />
		<div
			class="m-auto flex h-full w-full max-w-3xl flex-col items-start justify-start gap-4 p-16"
		>
			<Typography variant="title-md" class="mb-0">
				Please enter the key for this team
			</Typography>
			<Input bind:value={teamKey} placeholder="sp-critino-team-..." />
			<Button
				on:click={() => {
					authenticated = authenticateTeam();
				}}
			>
				Enter
			</Button>
		</div>
	</div>
{:else}<slot />{/if}
