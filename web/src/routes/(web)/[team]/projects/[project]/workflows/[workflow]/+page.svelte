<script lang="ts">
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	export let data;

	let { team, project, workflow } = data;
</script>

<Breadcrumb
	crumbs={[
		{ name: team.name, href: '/' },
		{ name: 'projects', href: '/projects' },
		{ name: project.name, href: `/projects/${project.name}` },
		{ name: 'workflows', href: `/projects/${project.name}/workflows` },
		{ name: workflow.name },
	]}
/>

<div class="m-auto flex items-center justify-center">Workflow {workflow.name} Dashboard</div>
