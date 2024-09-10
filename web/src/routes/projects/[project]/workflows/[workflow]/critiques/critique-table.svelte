<script lang="ts">
	import { createRender, createTable, Render, Subscribe } from 'svelte-headless-table';
	import {
		addHiddenColumns,
		addSelectedRows,
		addPagination,
		addSortBy,
		addTableFilter,
	} from 'svelte-headless-table/plugins';
	import ArrowUpDown from 'lucide-svelte/icons/arrow-up-down';
	import * as Table from '$lib/components/ui/table';
	import { Button } from '$lib/components/ui/button/index.js';
	import CritiqueTableActions from './critique-table-actions.svelte';
	import type { Critique, Database, Project, Workflow } from '$lib/supabase';
	import { readable } from 'svelte/store';
	import type { SupabaseClient } from '@supabase/supabase-js';

	export let supabase: SupabaseClient<Database>;
	export let project: Project;
	export let workflow: Workflow;
	export let critiques: Critique[];

	let table = createTable(readable(critiques), {
		page: addPagination({ initialPageSize: 10 }),
		sort: addSortBy(),
		filter: addTableFilter({
			fn: ({ filterValue, value }) => value.includes(filterValue),
		}),
		hiddenColumns: addHiddenColumns(),
		selectedRows: addSelectedRows(),
	});

	const columns = table.createColumns([
		table.column({
			accessor: 'created_at',
			header: 'Date',
			cell: ({ value }) => {
				return new Date(value).toLocaleDateString();
			},
		}),
		table.column({
			accessor: 'agent_name',
			header: 'Agent',
		}),
		table.column({
			accessor: ({ response }) => response,
			header: 'Response',
		}),
		table.column({
			accessor: ({ optimal }) => optimal,
			header: 'Optimal Response',
		}),
		table.column({
			accessor: ({ id }) => id,
			header: 'actions',
			cell: ({ value: id }) => {
				return createRender(CritiqueTableActions, {
					supabase,
					id,
					project,
					workflow,
					critiques,
				});
			},
		}),
	]);

	const { headerRows, pageRows, tableAttrs, tableBodyAttrs, pluginStates } =
		table.createViewModel(columns);

	const { hasNextPage, hasPreviousPage, pageIndex } = pluginStates.page;
</script>

{#if table}
	<div class="flex w-full items-center justify-center gap-4">
		<Table.Root {...$tableAttrs}>
			<Table.Header>
				{#each $headerRows as headerRow}
					<Subscribe rowAttrs={headerRow.attrs()}>
						<Table.Row class="border-surface-variant/80">
							{#each headerRow.cells as cell (cell.id)}
								<Subscribe
									attrs={cell.attrs()}
									let:attrs
									props={cell.props()}
									let:props
								>
									<Table.Head {...attrs}>
										{#if cell.id === 'actions'}{:else}
											<Button variant="ghost" on:click={props.sort.toggle}>
												<Render of={cell.render()} />
												<ArrowUpDown class={'ml-2 h-4 w-4'} />
											</Button>
										{/if}
									</Table.Head>
								</Subscribe>
							{/each}
						</Table.Row>
					</Subscribe>
				{/each}
			</Table.Header>
			<Table.Body {...$tableBodyAttrs}>
				{#each $pageRows as row (row.id)}
					<Subscribe rowAttrs={row.attrs()} let:rowAttrs>
						<Table.Row class="border-surface-variant/80" {...rowAttrs}>
							{#each row.cells as cell (cell.id)}
								<Subscribe attrs={cell.attrs()} let:attrs>
									<Table.Cell
										class="text-elipsis max-w-96 overflow-hidden"
										{...attrs}
									>
										<Render of={cell.render()} />
									</Table.Cell>
								</Subscribe>
							{/each}
						</Table.Row>
					</Subscribe>
				{/each}
			</Table.Body>
		</Table.Root>
	</div>
	{#if $hasNextPage || $hasPreviousPage}
		<div class="flex items-center justify-center space-x-4 py-4">
			<Button
				variant="outline"
				size="sm"
				on:click={() => ($pageIndex = $pageIndex - 1)}
				disabled={!$hasPreviousPage}
			>
				Previous
			</Button>
			<Button
				variant="outline"
				size="sm"
				disabled={!$hasNextPage}
				on:click={() => ($pageIndex = $pageIndex + 1)}
			>
				Next
			</Button>
		</div>
	{/if}
{/if}
