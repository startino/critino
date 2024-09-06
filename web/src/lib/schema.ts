import { z } from 'zod';
import type { Json } from './supabase';

const ZodJson: z.ZodSchema<Json> = z.lazy(() =>
	z.union([z.string(), z.number(), z.boolean(), z.null(), z.array(ZodJson), z.record(ZodJson)])
);

export const critiqueSchema = z.object({
	id: z.string(),
	agent_name: z.string(),
	workflow_name: z.string(),
	project_name: z.string(),
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
