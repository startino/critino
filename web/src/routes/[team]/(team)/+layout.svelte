<script lang="ts">
	import { Typography } from '$lib/components/ui/typography';
	import { sha256 } from 'js-sha256';
	import { afterUpdate, onMount } from 'svelte';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Button } from '$lib/components/ui/button';
	import { toast } from 'svelte-sonner';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb/index.js';

	export let data;

	$: ({ authenticated, team } = data);

	let newKey = '';
</script>

{#if !authenticated}
	<div class="relative flex w-full flex-col overflow-hidden">
		<Breadcrumb />
		<div
			class="m-auto flex h-full w-full max-w-3xl flex-col items-start justify-start gap-4 p-16"
		>
			<Typography variant="title-md" class="mb-0">
				Please enter the key for this team
			</Typography>
			<Input bind:value={newKey} placeholder="sp-critino-team-..." />
			<Button
				on:click={() => {
					window.location.href = window.location.href.split('?')[0] + `?key=${newKey}`;
				}}
			>
				Enter
			</Button>
		</div>
	</div>
{:else}<slot />{/if}
