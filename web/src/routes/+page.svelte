<script lang="ts">
	import { Separator } from '$lib/components/ui/separator';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';

	export let data;

	let { team } = data;
</script>

<div class="w-full">
	<div class="flex h-14 items-center px-4">
		<Breadcrumb crumbs={[{ name: team.name }, { name: 'home' }]} />
	</div>
	<Separator class="mt-0 pt-0 opacity-40" />
	<div class="flex h-full w-full items-center justify-center">Home Dashboard</div>
</div>
