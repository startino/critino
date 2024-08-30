<script lang="ts">
	import '$styling';
	import { Toaster } from '$lib/components/ui/sonner';
	import { setContext } from '$lib/context';
	import { Typography } from '$lib/components/ui/typography';
	import { invalidate } from '$app/navigation';
	import { onMount } from 'svelte';

	export let data;
	setContext('forms', data.forms);

	$: ({ user, supabase } = data);

	onMount(() => {
		const { data } = supabase.auth.onAuthStateChange((_, newUser) => {
			if (newUser?.expires_at !== user?.expires_at) {
				invalidate('supabase:auth');
			}
		});

		return () => data.subscription.unsubscribe();
	});
</script>

<Toaster />

<Typography class="absolute top-2 w-full text-center" variant="body-sm">
	logged in as {user.id}
</Typography>

<slot />
