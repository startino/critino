<script lang="ts">
	import { Typography } from '$lib/components/ui/typography';
	import { sha256 } from 'js-sha256';
	import { afterUpdate, onMount } from 'svelte';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Button } from '$lib/components/ui/button';
	import { toast } from 'svelte-sonner';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb/index.js';
	import { Separator } from '$lib/components/ui/separator';

	export let data;

	$: ({ team } = data);

	let authenticated = false;

	let key = '';

	const persistentAuth = () => {
		if (!team) {
			return;
		}
		if (!team.key) {
			authenticated = true;
			return;
		}

		if (sha256.update(localStorage.getItem('key' + team.name) ?? '').hex() !== team.key) {
			authenticated = false;
			return;
		}
		authenticated = true;
	};

	const authenticate = () => {
		authenticated = false;
		if (!team) {
			return;
		}
		if (!team.key) {
			authenticated = true;
			return;
		}
		if (sha256.update(key).hex() !== team.key) {
			key = localStorage.getItem('key' + team.name) ?? '';
			if (sha256.update(key).hex() !== team.key) {
				toast.error('Invalid key.');
				return;
			}
		}

		localStorage.setItem('key' + team.name, key!);
		authenticated = true;
	};

	onMount(() => {
		persistentAuth();
	});

	afterUpdate(() => {
		persistentAuth();
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
			<Input bind:value={key} placeholder="sp-critino-..." />
			<Button
				on:click={() => {
					authenticate();
				}}
			>
				Enter
			</Button>
		</div>
	</div>
{:else}<slot />{/if}
