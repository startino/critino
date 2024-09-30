<script lang="ts">
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import { Button } from '$lib/components/ui/button';
	import { Typography } from '$lib/components/ui/typography';
	import { sha256 } from 'js-sha256';
	import { onMount } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { v4 as uuidv4 } from 'uuid';

	export let data;

	$: ({ supabase, team } = data);

	let key: string | null = null;
	const genKey = async () => {
		key =
			'sp-critino-team-' +
			sha256.update(uuidv4().replace('-', '') + uuidv4().replace('-', '')).hex();

		const encryptedKey = key ? sha256.update(key).hex() : null;

		const { error: eTeam } = await supabase
			.from('teams')
			.update({
				key: encryptedKey,
			})
			.eq('name', team.name);

		if (eTeam) {
			console.error(`Error updating team key\nError: ${JSON.stringify(eTeam, null, 2)}`);
			toast.error('Error updating team key');
			return;
		}

		localStorage.setItem('key' + team.name, key);
	};

	const deleteKey = async () => {
		const storedKey = localStorage.getItem('key' + team.name);
		if (!storedKey) {
			toast.error('No key found to delete');
			return;
		}

		const { error: eTeam } = await supabase
			.from('teams')
			.update({
				key: null,
			})
			.eq('name', team.name);

		if (eTeam) {
			console.error(`Error deleting team key\nError: ${JSON.stringify(eTeam, null, 2)}`);
			toast.error('Error deleting team key');
			return;
		}

		localStorage.removeItem('key' + team.name);
		key = null;
		toast.success('Key deleted successfully');
	};

	onMount(() => {
		key = localStorage.getItem('key' + team.name) ?? null;
	});
</script>

<Breadcrumb />

<div class="m-auto flex h-full w-full max-w-3xl flex-col items-start justify-start gap-4 p-16">
	<Typography align="left" variant="headline-lg">{team.name}'s settings</Typography>

	<div class="mr-auto flex gap-2">
		<Button on:click={genKey}>Generate Access Key</Button>
		<Button variant="destructive" on:click={deleteKey}>Delete Key</Button>
	</div>

	{#if key}
		<div class="flex items-center justify-start gap-1">
			<Typography variant="title-sm">Key:</Typography>
			<Typography variant="body-sm" class="pt-1 text-left">
				{key}
			</Typography>
		</div>
		<Typography align="left" class="w-full text-wrap text-destructive">
			Save this key, it is required to access your team's administrative settings along with
			creating new root environments.
		</Typography>
	{/if}
</div>
