<script lang="ts">
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import { Button } from '$lib/components/ui/button';
	import { Typography } from '$lib/components/ui/typography';
	import { sha256 } from 'js-sha256';
	import { onMount } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { v4 as uuidv4 } from 'uuid';

	export let data;

	$: ({ supabase, environment } = data);

	let key: string | null = null;
	const genKey = async () => {
		key =
			'sp-critino-env-' +
			sha256.update(uuidv4().replace('-', '') + uuidv4().replace('-', '')).hex();

		const encryptedKey = key ? sha256.update(key).hex() : null;

		const { error: eenvironment } = await supabase
			.from('environments')
			.update({
				key: encryptedKey,
			})
			.eq('name', environment.name);

		if (eenvironment) {
			console.error(
				`Error updating environment key\nError: ${JSON.stringify(eenvironment, null, 2)}`
			);
			toast.error('Error updating environment key');
			return;
		}

		localStorage.setItem('key' + environment.name, key);
	};

	const deleteKey = async () => {
		const { error: eenvironment } = await supabase
			.from('environments')
			.update({
				key: null,
			})
			.eq('name', environment.name);

		if (eenvironment) {
			console.error(
				`Error deleting environment key\nError: ${JSON.stringify(environment, null, 2)}`
			);
			toast.error('Error deleting environment key');
			return;
		}
		key = null;
		toast.success('Key deleted successfully');

		if (localStorage.getItem('key' + environment.name)) {
			localStorage.removeItem('key' + environment.name);
		}
	};

	onMount(() => {
		key = localStorage.getItem('key' + environment.name) ?? null;
	});
</script>

<div class="m-auto flex h-full w-full max-w-3xl flex-col items-start justify-start gap-4 p-16">
	<Typography align="left" variant="headline-lg">
		{environment.name.split('/').pop()}'s settings
	</Typography>

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
			Save this key, it is required to access everything in your environment.
		</Typography>
	{/if}
</div>
