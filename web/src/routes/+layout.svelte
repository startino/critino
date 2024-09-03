<script lang="ts">
	import '$styling';
	import { Toaster } from '$lib/components/ui/sonner';
	import { invalidate } from '$app/navigation';
	import { onMount } from 'svelte';
	import * as schemes from '$lib/theme/schemes';
	import ThemeSwitcher from './theme-switcher.svelte';
	import { getMode } from '$lib/theme/index.js';
	import SidePanel from './sidepanel.svelte';
	import { Separator } from '$lib/components/ui/separator/index.js';

	export let data;

	$: ({ user, supabase } = data);
	let { teams } = data;
	console.log('routes/+layout.svelte teams', JSON.stringify(teams));

	onMount(() => {
		if (typeof window !== 'undefined') {
			for (const css of schemes[getMode()]) {
				document.documentElement.style.setProperty(
					css.split(': ')[0],
					css.split(': ')[1].replace(';', '')
				);
			}
		}

		const { data } = supabase.auth.onAuthStateChange((_, newUser) => {
			if (newUser?.expires_at !== user?.expires_at) {
				invalidate('supabase:auth');
			}
		});

		return () => data.subscription.unsubscribe();
	});
</script>

<Toaster />

<div class="absolute right-2 top-2">
	<ThemeSwitcher />
</div>
<main class="flex h-screen w-screen items-stretch bg-background text-background-on">
	<SidePanel {teams} />
	<Separator orientation="vertical" class="ml-0 pl-0" />
	<div class="flex h-full w-full flex-col items-center justify-center">
		<slot />
	</div>
</main>
