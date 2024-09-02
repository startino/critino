<script lang="ts">
	import type { Icon } from 'lucide-svelte';

	type $$Props = Icon['$$prop_def'];
	type $$Events = Icon['$$events_def'];
	type $$Slots = Icon['$$slot_def'];

	export let src: string;
	export let alt: string;
</script>

<img {alt} {src} height="24" width="24" {...$$restProps} />
