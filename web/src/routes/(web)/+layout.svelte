<script lang="ts">
	import '$styling';
	import { Toaster } from '$lib/components/ui/sonner';
	import { invalidate } from '$app/navigation';
	import { onMount } from 'svelte';
	import * as schemes from '$lib/theme/schemes';
	import ThemeSwitcher from './theme-switcher.svelte';
	import { getMode } from '$lib/theme/index.js';

	export let data;

	$: ({ user, supabase } = data);

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

<div class="absolute right-2 top-2 z-10">
	<ThemeSwitcher />
</div>
<slot />
