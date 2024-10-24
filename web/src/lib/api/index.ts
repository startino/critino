import createClient from 'openapi-fetch';
import type { paths, components } from './v0.d.ts';
import { PUBLIC_API_URL } from '$env/static/public';
import { getURL } from '$lib/utils.ts';

const api = createClient<paths>({ baseUrl: getURL(PUBLIC_API_URL) });
export default api;

type schemas = components['schemas'];
type headers = components['headers'];
type responses = components['responses'];
type parameters = components['parameters'];
type requestBodies = components['requestBodies'];
type pathItems = components['pathItems'];
export type { paths, schemas, headers, responses, parameters, requestBodies, pathItems };
