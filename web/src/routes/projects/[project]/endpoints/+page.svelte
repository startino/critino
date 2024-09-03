<script lang="ts">
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import { Separator } from '$lib/components/ui/separator';
	import { Typography } from '$lib/components/ui/typography';
	export let data;

	let { team, project } = data;
</script>

<Breadcrumb
	crumbs={[
		{ name: team.name, href: '/' },
		{ name: 'projects', href: '/projects' },
		{ name: project.name, href: '/projects/' + project.name },
		{ name: 'endpoints' },
	]}
/>

<div class="flex w-full flex-col items-center justify-start">
	<Separator class="mt-0 pt-0 opacity-40" />
	<div class="flex h-full w-full flex-col">
		<div class="flex h-full w-full flex-col items-center justify-center">
			<Typography as="h2" variant="headline-sm">API Endpoints:</Typography>
			<Typography as="p" variant="body-md">
				GET /projects/{project.name}
			</Typography>
		</div>
	</div>
</div>
