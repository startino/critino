<script lang="ts">
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import { Separator } from '$lib/components/ui/separator';
	export let data;

	let { team, project } = data;
</script>

<Breadcrumb
	crumbs={[
		{ name: team.name, href: '/' },
		{ name: 'projects', href: '/projects' },
		{ name: project.name },
	]}
/>

<div class="flex w-full items-center justify-center">Project {project.name} Dashboard</div>
