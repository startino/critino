<script lang="ts">
	// NOTE: Best docs https://tiptap.dev/docs/editor/api/editor
	//
	import { createEventDispatcher, onDestroy, onMount } from 'svelte';
	import { type Props, variants } from './index';
	import { Editor } from '@tiptap/core';
	import StarterKit from '@tiptap/starter-kit';
	import HardBreak from '@tiptap/extension-hard-break';
	import { cn } from '$lib/utils';

	const dispatch = createEventDispatcher();

	type $$Props = Props;
	let className: $$Props['class'] = undefined;
	export { className as class };

	export let content: string = '';
	export let editable: boolean = true;

	$: if (editor && content !== editor.getHTML()) {
		editor.chain().setContent(content, false, { preserveWhitespace: 'full' }).run();
	}

	$: {
		if (editor) {
			editor.setEditable(editable);
		}
	}

	let element: Element;
	let editor: Editor;

	onMount(() => {
		editor = new Editor({
			element: element,
			extensions: [
				StarterKit,
				HardBreak.extend({
					addKeyboardShortcuts() {
						return {
							Enter: () => {
								dispatch('enter');
								return true; // prevent the default behavior
							},
							ShiftEnter: () => {
								this.editor.commands.setHardBreak();
								return true; // prevent the default behavior
							},
						};
					},
				}),
			],
			content: content,
			onTransaction: () => {
				// force re-render so `editor.isActive` works as expected
				editor = editor;

				if (content === editor.getHTML()) {
					return;
				}

				content = editor.getHTML();
			},
		});

		editor.setOptions({
			editorProps: {
				attributes: {
					class: cn(variants({ className })),
				},
			},
		});
	});

	onDestroy(() => {
		if (editor) {
			editor.destroy();
		}
	});
</script>

<div bind:this={element}></div>
