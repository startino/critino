import { z } from 'zod';
import type { Json } from './supabase';

const ZodJson: z.ZodSchema<Json> = z.lazy(() =>
	z.union([z.string(), z.number(), z.boolean(), z.null(), z.array(ZodJson), z.record(ZodJson)])
);

export const critiqueSchema = z.object({
	id: z.string(),
	agent_name: z.string(),
	workflow_name: z.string(),
	environment_name: z.string(),
	team_name: z.string(),
	response: z.string(),
	optimal: z.string(),
	context: z.array(
		z.object({
			name: z.string(),
			content: z.string(),
			index: z.number(),
		})
	),
	critique: ZodJson,
	tags: z.array(z.string()),
});

export type CritiqueSchema = typeof critiqueSchema;

export const environmentSchema = z.object({
	name: z
		.string()
		.min(2)
		.max(50)
		.regex(/^[^/]*$/, "Name must not contain '/'"),
	description: z.string().min(0).max(100),
	parent_name: z.string().nullable(),
});

export type FormSchema = typeof environmentSchema;
