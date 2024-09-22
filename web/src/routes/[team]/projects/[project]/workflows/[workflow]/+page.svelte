<script lang="ts">
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	export let data;

	let { team, project, workflow } = data;
</script>

<Breadcrumb
	crumbs={[
		{ name: team.name, href: `/${team.name}` },
		{ name: 'projects', href: `/${team.name}/projects` },
		{ name: project.name, href: `/${team.name}/projects/${project.name}` },
		{ name: 'workflows', href: `/${team.name}/projects/${project.name}/workflows` },
		{ name: workflow.name },
	]}
/>

<div class="m-auto flex items-center justify-center">Workflow {workflow.name} Dashboard</div>
