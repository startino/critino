<script lang="ts">
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
</script>

<Breadcrumb />
<div class="flex h-full w-full">
	<div class="relative flex w-full flex-col overflow-hidden text-nowrap">
		<slot />
	</div>
</div>
