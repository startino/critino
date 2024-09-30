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

	$: ({ supabase, team, params, environment, environments: allEnvironments, workflows } = data);

	$: environments = allEnvironments.filter((env) => env.name.startsWith(params.env + '/'));

	let envKey = '';

	const persistentAuthEnv = () => {
		if (!environment) {
			return false;
		}
		if (!environment.key) {
			return false;
		}

		if (
			sha256
				.update(localStorage.getItem('key' + team.name + environment.name) ?? '')
				.hex() !== environment.key
		) {
			return false;
		}

		return true;
	};

	const authenticateEnv = () => {
		if (!environment) {
			return false;
		}
		if (!environment.key) {
			return false;
		}
		if (sha256.update(envKey).hex() !== environment.key) {
			envKey = localStorage.getItem('key' + team.name + environment.name) ?? '';
			if (sha256.update(envKey).hex() !== environment.key) {
				return false;
			}
		}

		localStorage.setItem('key' + team.name + environment.name, envKey!);
		return true;
	};

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
		if (!authenticated) {
			authenticated = persistentAuthEnv();
		}
	});

	afterUpdate(() => {
		authenticated = false;
		authenticated = persistentAuthTeam();
		if (!authenticated) {
			authenticated = persistentAuthEnv();
		}
	});
</script>

<div class="flex h-full w-full">
	{#if !authenticated}
		<div class="relative flex w-full flex-col overflow-hidden text-nowrap">
			<Breadcrumb />
			<div
				class="m-auto flex h-full w-full max-w-3xl flex-col items-start justify-start gap-4 p-16"
			>
				<Typography variant="title-md" class="mb-0">
					Please enter the key for this environment
				</Typography>
				<Input bind:value={envKey} placeholder="sp-critino-env-..." />
				<Button
					on:click={() => {
						authenticated = authenticateTeam();
						if (!authenticated) {
							authenticated = authenticateEnv();
						}
						if (!authenticated) {
							toast.error('Invalid team and env key');
						}
					}}
				>
					Enter
				</Button>
			</div>
		</div>
	{:else}
		<!-- Nav -->
		<div class="flex h-full w-64 flex-col items-start justify-start">
			<div class="flex h-14 w-full items-center justify-start px-4">
				<Typography
					variant="title-md"
					overflow="ellipsis"
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

		<div class="relative flex max-h-screen w-full flex-col overflow-x-hidden text-nowrap">
			<Breadcrumb />
			<slot />
		</div>
	{/if}
</div>
