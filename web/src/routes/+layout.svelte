<script lang="ts">
	import '$styling';
	import { Toaster } from '$lib/components/ui/sonner';
	import TeamSwitcher from './team-switcher.svelte';
	import { invalidate } from '$app/navigation';
	import { onMount } from 'svelte';
	import Nav from './nav.svelte';
	import * as Resizable from '$lib/components/ui/resizable';
	import { Separator } from '$lib/components/ui/select';
	import { primaryRoutes, profileRoutes, teamRoutes } from './routes';
	import { cn } from '$lib/utils';
	import { Typography } from '$lib/components/ui/typography/index.js';
	import * as schemes from '$lib/theme/schemes';
	import ThemeSwitcher from './theme-switcher.svelte';
	import { getMode } from '$lib/theme/index.js';

	export let data;

	$: ({ user, supabase, teams } = data);
	console.log(JSON.stringify(teams));

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

	export let navCollapsedSize: number;

	let isCollapsed = true;
	function onCollapse() {
		isCollapsed = true;
	}
	function onExpand() {
		isCollapsed = false;
	}
</script>

<Toaster />

<main class="h-screen w-screen bg-background text-background-on">
	<div class="absolute right-2 top-2">
		<ThemeSwitcher />
	</div>
	<div class="h-full w-full md:block">
		<Resizable.PaneGroup direction="horizontal" class="h-full items-stretch">
			<Resizable.Pane
				collapsedSize={navCollapsedSize}
				collapsible
				defaultSize={0}
				minSize={20}
				maxSize={20}
				class="flex min-w-14 flex-col"
				{onCollapse}
				{onExpand}
			>
				<div
					class={cn(
						'flex h-14 flex-col items-center justify-center',
						isCollapsed ? 'w-14' : 'px-2'
					)}
				>
					<TeamSwitcher {isCollapsed} {teams} />
				</div>
				<Separator />
				<Nav {isCollapsed} routes={primaryRoutes} />
				<Separator />
				<Typography
					align="left"
					variant="title-md"
					class={cn('self-center px-4 pt-2', isCollapsed ? 'block' : 'hidden')}
				>
					T
				</Typography>
				<Typography
					align="left"
					variant="body-lg"
					class={cn('px-4 pt-2', isCollapsed ? 'hidden' : 'block')}
				>
					Team Management
				</Typography>
				<Nav {isCollapsed} routes={teamRoutes} />
				<Separator />
				<Typography
					align="left"
					variant="title-md"
					class={cn('self-center px-4 pt-2', isCollapsed ? 'block' : 'hidden')}
				>
					P
				</Typography>
				<Typography
					align="left"
					variant="body-lg"
					class={cn('px-4 pt-2', isCollapsed ? 'hidden' : 'block')}
				>
					Profile Management
				</Typography>
				<Nav {isCollapsed} routes={profileRoutes} />
			</Resizable.Pane>
			<Resizable.Handle withHandle />
			<slot />
		</Resizable.PaneGroup>
	</div>
</main>
