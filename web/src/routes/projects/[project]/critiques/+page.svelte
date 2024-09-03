<script lang="ts">
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import { Separator } from '$lib/components/ui/separator';
	export let data;

	let { team, project } = data;
</script>

<div class="flex h-14 w-full items-center justify-start px-4">
	<Breadcrumb
		crumbs={[
			{ name: team.name, href: '/' },
			{ name: 'projects', href: '/projects' },
			{ name: project.name, href: '/projects/' + project.name },
			{ name: 'critiques' },
		]}
	/>
</div>

<Separator class="mt-0 pt-0 opacity-40" />

<div class="flex h-full w-full flex-col">Not Build Yet</div>
