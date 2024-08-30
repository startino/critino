<script lang="ts">
	import { Typography } from '.';
</script>

<div class="flex h-screen items-center justify-center gap-8">
	<div class="flex h-fit items-end justify-end gap-8">
		<div class="leading- flex h-full flex-col items-start justify-start">
			<Typography as="p" variant="display-lg">display lg</Typography>
			<Typography as="p" variant="display-md">display md</Typography>
			<Typography as="p" variant="display-sm">display sm</Typography>
		</div>
		<div class="flex h-full flex-col items-start justify-start gap-4">
			<div class="flex flex-col">
				<Typography as="p" variant="headline-lg">headline lg</Typography>
				<Typography as="p" variant="body-lg">body lg</Typography>
			</div>
			<div class="flex flex-col">
				<Typography as="p" variant="headline-md">headline md</Typography>
				<Typography as="p" variant="body-md">body md</Typography>
			</div>
			<div class="flex flex-col">
				<Typography as="p" variant="headline-sm">headline sm</Typography>
				<Typography as="p" variant="body-sm">body sm</Typography>
			</div>
		</div>
		<div class="items-between flex h-full flex-col justify-between gap-4">
			<div class="flex flex-col">
				<Typography as="p" variant="title-lg">title lg</Typography>
				<Typography as="p" variant="body-lg">body lg</Typography>
			</div>
			<div class="flex flex-col">
				<Typography as="p" variant="title-md">title md</Typography>
				<Typography as="p" variant="body-md">body md</Typography>
			</div>
			<div class="flex flex-col">
				<Typography as="p" variant="title-sm">title sm</Typography>
				<Typography as="p" variant="body-sm">body sm</Typography>
			</div>
		</div>
		<div class="flex flex-col items-start justify-start">
			<Typography as="p" variant="body-lg">body lg</Typography>
			<Typography as="p" variant="body-md">body md</Typography>
			<Typography as="p" variant="body-sm">body sm</Typography>
		</div>
	</div>
</div>
