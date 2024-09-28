<script lang="ts">
	import { Separator } from '$lib/components/ui/separator';
	import * as Card from '$lib/components/ui/card';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import { goto } from '$app/navigation';
	import { ChevronRight, Plus } from 'lucide-svelte';
	import { TipTap } from '$lib/components/ui/tiptap';

	export let data;

	let { team, params } = data;
</script>

<Breadcrumb crumbs={[{ name: team.name, href: `/${team.name}` }, { name: 'environments' }]} />

<div>
	<div
		class="grid h-fit w-full grid-cols-1 items-start justify-center gap-4 p-4 sm:grid-cols-1 md:grid-cols-1 lg:grid-cols-2 xl:grid-cols-3"
	>
		<h1>{params.env}</h1>
	</div>
</div>
