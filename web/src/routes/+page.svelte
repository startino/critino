<script lang="ts">
	import * as Resizable from '$lib/components/ui/resizable';
	import * as Tabs from '$lib/components/ui/tabs';
	import { Separator } from '$lib/components/ui/select';
	import { Typography } from '$lib/components/ui/typography';

	export let defaultSize = 440;
</script>

<Resizable.Pane {defaultSize}>
	<Tabs.Root value="all">
		<div class="flex h-14 items-center px-4">
			<Typography as="h1" variant="title-lg">Home</Typography>
		</div>
		<Separator />
		<div class="flex h-full w-full items-center justify-center">Home Dashboard</div>
	</Tabs.Root>
</Resizable.Pane>
