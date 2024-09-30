<script lang="ts">
	import Nav from '$lib/components/ui/nav.svelte';
	import { Separator } from '$lib/components/ui/separator';
	import { Typography } from '$lib/components/ui/typography';
	import { sha256 } from 'js-sha256';
	import { primaryRoutes } from './routes';
	import { afterUpdate, onMount } from 'svelte';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Button } from '$lib/components/ui/button';
	import { toast } from 'svelte-sonner';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';

	export let data;

	$: ({ supabase, team, params, environments: allEnvironments, workflows } = data);

	$: environments = allEnvironments.filter((env) => env.name.startsWith(params.env + '/'));

	$: environment = allEnvironments.find((env) => env.name === params.env);

	let authenticated = false;

	let key = '';

	const persistentAuth = () => {
		if (environment) {
			if (environment.key) {
				if (
					sha256.update(localStorage.getItem('key' + environment.name) ?? '').hex() !==
					environment.key
				) {
					authenticated = false;
					return;
				}
				authenticated = true;
			} else {
				authenticated = true;
			}
		}
	};

	const authenticate = () => {
		authenticated = false;
		if (environment) {
			if (environment.key) {
				if (sha256.update(key).hex() !== environment.key) {
					key = localStorage.getItem('key' + environment.name) ?? '';
					if (sha256.update(key).hex() !== environment.key) {
						toast.error('Invalid key.');
						return;
					}
				}

				localStorage.setItem('key' + environment.name, key!);
				authenticated = true;
			} else {
				authenticated = true;
			}
		}
	};

	onMount(() => {
		persistentAuth();
	});

	afterUpdate(() => {
		persistentAuth();
	});
</script>

<div class="flex h-full w-full">
	<!-- Nav -->
	<div class="flex h-full w-64 flex-col items-start justify-start">
		<div class="flex h-14 w-full items-center justify-start px-4">
			<Typography
				variant="title-md"
				class="mb-0 w-full overflow-hidden text-ellipsis pb-0 text-left"
			>
				{environment.name.split('/').pop()}
			</Typography>
		</div>
		<Separator class="mt-0 pt-0 opacity-20" />

		<Nav routes={primaryRoutes(team, environments, environment, workflows)} />
	</div>

	<Separator orientation="vertical" class="ml-0 pl-0 opacity-20" />
	<!-- /Nav -->

	{#if !authenticated}
		<div class="relative flex w-full flex-col overflow-hidden text-nowrap">
			<div
				class="m-auto flex h-full w-full max-w-3xl flex-col items-start justify-start gap-4 p-16"
			>
				<Breadcrumb />
				<Typography variant="title-md" class="mb-0">
					Please enter the key for this environment
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
	{:else}
		<div class="relative flex w-full flex-col overflow-hidden text-nowrap">
			<Breadcrumb />
			<slot />
		</div>
	{/if}
</div>
