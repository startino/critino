import { z } from 'zod';

export const formSchema = z.object({
	name: z
		.string()
		.min(2)
		.max(50)
		.regex(/^[^/]*$/, "Name must not contain '/'"),
	description: z.string().min(0).max(100),
});

export type FormSchema = typeof formSchema;
