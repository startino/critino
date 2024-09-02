<script lang="ts">
	import * as Resizable from '$lib/components/ui/resizable';
	import { Separator } from '$lib/components/ui/separator';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	import { Typography } from '$lib/components/ui/typography';

	export let data;

	let { team, project } = data;
</script>

<div class="w-full">
	<div class="flex h-14 items-center justify-start px-4">
		<Breadcrumb
			crumbs={[
				{ name: team.name, href: '/' },
				{ name: 'projects', href: '/projects' },
				{ name: project.name },
			]}
		/>
	</div>
	<Separator class="mt-0 pt-0 opacity-40" />

	<div class="flex h-full w-full flex-col items-center justify-center">
		<Typography as="h1" variant="headline-lg">{project.name}</Typography>
		<Typography as="h2" variant="headline-sm">API Endpoints:</Typography>
		<Typography as="p" variant="body-md">
			GET /projects/{project.name}
		</Typography>
	</div>
</div>
