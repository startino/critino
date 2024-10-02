<script lang="ts">
	import { goto } from '$app/navigation';
	import { toast } from 'svelte-sonner';

	import { Button } from '$lib/components/ui/button';
	import { Pencil, Trash2 } from 'lucide-svelte';
	import type { Critique, Database, Environment, Workflow } from '$lib/supabase';
	import type { SupabaseClient } from '@supabase/supabase-js';

	type Props = {
		supabase: SupabaseClient<Database>;
		id: string;
		environment: Environment;
		workflow: Workflow;
		critiques: Critique[];
	};

	let { supabase, id, environment, workflow, critiques }: Props = $props();

	const handleDelete = async (id: string) => {
		const { error: e } = await supabase.from('critiques').delete().eq('id', id);

		if (e) {
			const message = `Error deleting critique: ${JSON.stringify(e, null, 2)}`;
			console.error(message);
			toast.error(message);
			return;
		}
		critiques = critiques.filter((critique) => critique.id !== id);

		toast.success('Critique deleted!');
	};
</script>

<div class="flex flex-shrink justify-end gap-1">
	<Button
		variant="ghost"
		class="aspect-1 p-1 text-primary hover:bg-transparent hover:text-primary-container-on"
		on:click={() => goto(`${workflow.name}/${id}`)}
	>
		<Pencil></Pencil>
	</Button>
	<Button
		variant="ghost"
		class="aspect-1 p-1 text-error hover:bg-transparent hover:text-error-container-on"
		on:click={() => handleDelete(id)}
	>
		<Trash2></Trash2>
	</Button>
</div>
