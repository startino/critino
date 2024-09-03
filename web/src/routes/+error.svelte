<script>
	import { Separator } from '$lib/components/ui/separator';
	import { Typography } from '$lib/components/ui/typography';

	import { page } from '$app/stores';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
</script>

<div class="flex h-full w-full flex-col text-error">
	<div class="flex h-16 w-full items-center justify-start px-4">
		<Typography variant="title-lg" class="mb-0 pb-0">Error</Typography>
	</div>
	<Separator class="mt-0 pt-0 opacity-40" />

	<div class="flex flex-1 flex-col items-center justify-center">
		<Typography variant="headline-lg">Status: {$page.status}</Typography>
		<Typography variant="title-lg">Message: {$page.error.message}</Typography>
	</div>
	<Separator />

	<Typography variant="headline-sm">Debug</Typography>
	<div class="relative h-full w-full flex-grow">
		<ScrollArea class="absolute bottom-0 left-0 right-0 top-0 overflow-hidden">
			<pre>{JSON.stringify($page, null, 2)}</pre>
		</ScrollArea>
	</div>
</div>
