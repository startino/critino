<script lang="ts">
	import * as Card from '$lib/components/ui/card';
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
	import type { Critique, Database, Environment, Workflow } from '$lib/supabase';
	import { readable } from 'svelte/store';
	import type { SupabaseClient } from '@supabase/supabase-js';
	import { TipTap } from '$lib/components/ui/tiptap';
	import * as Tooltip from '$lib/components/ui/tooltip';
	import TooltipContent from '$lib/components/ui/tooltip/tooltip-content.svelte';

	export let supabase: SupabaseClient<Database>;
	export let environment: Environment;
	export let workflow: Workflow;
	export let critiques: Critique[];
	export let agent: string;

	const filteredCritiques: Critique[] = critiques.filter(
		(critique) => critique.agent_name === agent
	);

	let table = createTable(readable(filteredCritiques), {
		page: addPagination({ initialPageSize: 6 }),
		sort: addSortBy(),
		filter: addTableFilter({
			fn: ({ filterValue, value }) => value.includes(filterValue),
		}),
		hiddenColumns: addHiddenColumns(),
		selectedRows: addSelectedRows(),
	});

	const columns = table.createColumns([
		table.column({
			accessor: ({ id }) => id,
			header: 'actions',
			cell: ({ value: id }) => {
				return createRender(CritiqueTableActions, {
					supabase,
					id,
					environment,
					workflow,
					critiques: filteredCritiques,
				});
			},
		}),
		table.column({
			accessor: 'query',
			header: 'Query',
		}),
		table.column({
			accessor: 'optimal',
			header: 'Optimal Response',
		}),
		table.column({
			accessor: 'response',
			header: 'Original Response',
		}),
		table.column({
			accessor: 'created_at',
			header: 'Date',
			cell: ({ value }) => {
				return new Date(value).toLocaleDateString();
			},
		}),
	]);

	const { headerRows, pageRows, tableAttrs, tableBodyAttrs, pluginStates } =
		table.createViewModel(columns);

	const { hasNextPage, hasPreviousPage, pageIndex } = pluginStates.page;
</script>

<Card.Root class="mx-auto h-full w-full border-surface-variant/80 bg-primary/5 text-left">
	<Card.Header class="border-b border-surface-variant/80">
		<Card.Title>{agent}'s critiques</Card.Title>
	</Card.Header>
	<Card.Content class="p-0">
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
													<Button
														variant="ghost"
														on:click={props.sort.toggle}
													>
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
								<Table.Row class=" border-surface-variant/80" {...rowAttrs}>
									{#each row.cells as cell (cell.id)}
										<Subscribe attrs={cell.attrs()} let:attrs>
											{#if cell.id === 'response' || cell.id === 'optimal' || cell.id === 'query'}
												<Table.Cell
													class="max-h-[10ch] w-max max-w-[65ch] overflow-hidden text-ellipsis"
													{...attrs}
												>
													<Tooltip.Root>
														<Tooltip.Trigger>
															<TipTap
																class="max-h-[12ch] w-max max-w-[65ch] overflow-hidden text-ellipsis text-left text-background-on"
																editable={false}
																content={cell.render().toString()}
															></TipTap>
														</Tooltip.Trigger>
														<Tooltip.Content>
															<TipTap
																class="w-max max-w-prose text-left text-background-on"
																editable={false}
																content={cell.render().toString()}
															></TipTap>
														</Tooltip.Content>
													</Tooltip.Root>
												</Table.Cell>
											{:else}
												<Table.Cell
													class="text-elipsis overflow-hidden"
													{...attrs}
												>
													<Render of={cell.render()} />
												</Table.Cell>
											{/if}
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
	</Card.Content>
</Card.Root>
