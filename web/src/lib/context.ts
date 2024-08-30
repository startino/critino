import { getContext as getSvelteContext, setContext as setSvelteContext } from 'svelte';

export function setContext<K extends keyof ContextMap>(key: K, value: ContextMap[K]) {
	return setSvelteContext(key, value);
}

export function getContext<K extends keyof ContextMap>(key: K): ContextMap[K] {
	const svelteContext = getSvelteContext<ContextMap[K]>(key);
	return svelteContext;
}

export interface ContextMap {
	forms: FormsContext;
}

// Contexts:

export interface FormsContext {
}
