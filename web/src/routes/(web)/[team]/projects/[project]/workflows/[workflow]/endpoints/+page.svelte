<script lang="ts">
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import { Separator } from '$lib/components/ui/separator';
	import { Typography } from '$lib/components/ui/typography';
	import { getURL } from '$lib/utils.js';
	export let data;

	let { team, project, workflow } = data;
</script>

<Breadcrumb
	crumbs={[
		{ name: team.name, href: `/${team.name}` },
		{ name: 'projects', href: `/${team.name}/projects` },
		{ name: project.name, href: `/${team.name}/projects/${project.name}` },
		{ name: 'workflows', href: `/${team.name}/projects/${project.name}/workflows` },
		{
			name: workflow.name,
			href: `/${team.name}/projects/${project.name}/workflows/${workflow.name}`,
		},
		{ name: 'endpoints' },
	]}
/>

<div class="m-auto flex flex-col items-start justify-center gap-6">
	<Typography align="left" as="h1" variant="headline-sm">API Endpoints:</Typography>
	<Typography align="left" as="h1" variant="title-md" class="text-error-container-on">
		This page is for developers implementing critino.
		<br />
		If you are not a developer you do not have to worry about this page.
	</Typography>
	<Typography align="left" as="p" variant="body-md">
		{`POST: ${getURL()}${team.name}/${project.name}/${workflow.name}/[agent-name]`}
		<br />
		body:
		<br />
		- id: uuid(string) - used to prevent creation of duplicates
		<br />
		- response: string
		<br />
		- context: Json(name: string, content: string, index: number)[]
		<br />
		- tags: string[]
	</Typography>
</div>
