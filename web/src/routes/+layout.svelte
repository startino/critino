<script lang="ts">
	import '$styling';
	import { Toaster } from '$lib/components/ui/sonner';
	import { ModeWatcher } from 'mode-watcher';
	import { ModeSwitcher } from '$lib/components/ui/mode-switcher';
</script>

<Toaster />

<ModeWatcher />
<div class="absolute right-2 top-2 z-10">
	<ModeSwitcher />
</div>
<slot />
