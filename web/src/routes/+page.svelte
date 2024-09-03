<script lang="ts">
	import { Separator } from '$lib/components/ui/separator';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';

	export let data;

	let { team } = data;
</script>

<Breadcrumb crumbs={[{ name: team.name }, { name: 'home' }]} />
<Separator class="mt-14 opacity-20" />
<div class="flex w-full items-center justify-center">Home Dashboard</div>
