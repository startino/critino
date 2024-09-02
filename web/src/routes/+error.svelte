<script>
	import * as Resizable from '$lib/components/ui/resizable';
	import { Separator } from '$lib/components/ui/separator';
	import { Typography } from '$lib/components/ui/typography';

	import { page } from '$app/stores';
</script>

<Resizable.Pane class="flex flex-col text-error">
	<div class="flex h-14 items-center px-4">
		<Typography as="h1" variant="body-lg">Error</Typography>
	</div>
	<Separator />

	<div class="flex flex-1 flex-col items-center justify-center">
		<Typography variant="headline-lg">Status: {$page.status}</Typography>
		<Typography variant="title-lg">Message: {$page.error.message}</Typography>
	</div>
	<Separator />

	<Typography variant="headline-sm">Debug</Typography>
	<div class="max-h-96 overflow-scroll p-5 text-sm">
		<pre>{JSON.stringify($page, null, 2)}</pre>
	</div>
</Resizable.Pane>
