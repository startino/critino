<script lang="ts">
	import { type Props, typographyVariants } from './index';
	import { cn } from '$lib/utils';

	type $$Props = Props;

	export let as: $$Props['as'] = 'p';
	export let variant: $$Props['variant'] = 'body-md';
	export let align: $$Props['align'] = 'center';
	let className: $$Props['class'] = undefined;
	export { className as class };
</script>

<svelte:element this={as} class={cn(typographyVariants({ className, variant, align }))}>
	<slot />
</svelte:element>
