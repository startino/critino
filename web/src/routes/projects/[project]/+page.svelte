<script lang="ts">
	import * as Resizable from '$lib/components/ui/resizable';
	import { Separator } from '$lib/components/ui/select';
	import { Typography } from '$lib/components/ui/typography';

	export let data;

	let { team, project } = data;
</script>

<Resizable.Pane>
	<div class="flex h-14 items-center px-4">
		<Typography as="h1" variant="body-lg" class="flex items-center justify-center">
			{team.name}
			<span class="px-4 text-2xl opacity-30">/</span>
			projects
			<span class="px-4 text-2xl opacity-30">/</span>
			{project.name}
		</Typography>
	</div>
	<Separator />
	{JSON.stringify(project, null, 2)}
</Resizable.Pane>
