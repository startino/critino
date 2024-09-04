<script lang="ts">
	import { Separator } from '$lib/components/ui/separator';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';

	export let data;

	let { team } = data;
</script>

<Breadcrumb crumbs={[{ name: team.name }, { name: 'home' }]} />
<div class="m-auto flex items-center justify-center">Home Dashboard</div>
