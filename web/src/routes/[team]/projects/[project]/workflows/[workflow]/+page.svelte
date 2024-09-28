<script lang="ts">
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	export let data;

	let { team, environment, workflow } = data;
</script>

<Breadcrumb
	crumbs={[
		{ name: team.name, href: `/${team.name}` },
		{ name: 'environments', href: `/${team.name}/environments` },
		{ name: environment.name, href: `/${team.name}/environments/${environment.name}` },
		{ name: 'workflows', href: `/${team.name}/environments/${environment.name}/workflows` },
		{ name: workflow.name },
	]}
/>

<div class="m-auto flex items-center justify-center">Workflow {workflow.name} Dashboard</div>
