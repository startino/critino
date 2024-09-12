<script lang="ts">
	import Sun from 'lucide-svelte/icons/sun';
	import Moon from 'lucide-svelte/icons/moon';

	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import { Button } from '$lib/components/ui/button';
	import { getMode, resetMode, setMode, system } from '$lib/theme';

	let mode = getMode();
</script>

<DropdownMenu.Root>
	<DropdownMenu.Trigger asChild let:builder>
		<Button builders={[builder]} variant="outline" size="icon">
			{#if mode.includes('light')}
				<Sun class="h-[1.2rem] w-[1.2rem] text-primary transition-all" />
			{:else}
				<Moon class="h-[1.2rem] w-[1.2rem] text-primary transition-all" />
			{/if}
			<span class="sr-only">Toggle theme</span>
		</Button>
	</DropdownMenu.Trigger>
	<DropdownMenu.Content align="end">
		<DropdownMenu.Item
			on:click={() => {
				setMode('light'), (mode = 'light');
			}}
		>
			Light
		</DropdownMenu.Item>
		<DropdownMenu.Item
			on:click={() => {
				setMode('lightMediumContrast'), (mode = 'lightMediumContrast');
			}}
		>
			Light Medium Contrast
		</DropdownMenu.Item>
		<DropdownMenu.Item
			on:click={() => {
				setMode('lightHighContrast'), (mode = 'lightHighContrast');
			}}
		>
			Light High Contrast
		</DropdownMenu.Item>
		<DropdownMenu.Item
			on:click={() => {
				setMode('dark'), (mode = 'dark');
			}}
		>
			Dark
		</DropdownMenu.Item>
		<DropdownMenu.Item
			on:click={() => {
				setMode('darkMediumContrast'), (mode = 'darkMediumContrast');
			}}
		>
			Dark Medium Contrast
		</DropdownMenu.Item>
		<DropdownMenu.Item
			on:click={() => {
				setMode('darkHighContrast'), (mode = 'darkHighContrast');
			}}
		>
			Dark High Contrast
		</DropdownMenu.Item>
		<DropdownMenu.Item
			on:click={() => {
				resetMode(), (mode = system());
			}}
		>
			System
		</DropdownMenu.Item>
	</DropdownMenu.Content>
</DropdownMenu.Root>
