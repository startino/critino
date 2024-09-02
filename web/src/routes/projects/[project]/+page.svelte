<script lang="ts">
	import * as Resizable from '$lib/components/ui/resizable';
	import { Separator } from '$lib/components/ui/separator';
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';

	export let data;

	let { team, project } = data;
</script>

<Resizable.Pane>
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
	{JSON.stringify(project, null, 2)}
</Resizable.Pane>
