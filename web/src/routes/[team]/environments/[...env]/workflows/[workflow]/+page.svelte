<script lang="ts">
	import { Breadcrumb } from '$lib/components/ui/breadcrumb';
	export let data;

	let { team, environment, workflow } = data;
</script>

<Breadcrumb />

<div class="m-auto flex items-center justify-center">Workflow {workflow.name} Dashboard</div>
