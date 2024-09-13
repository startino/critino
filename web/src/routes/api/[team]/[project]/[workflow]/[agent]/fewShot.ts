import { FewShotPromptTemplate, PromptTemplate } from '@langchain/core/prompts';
import { SemanticSimilarityExampleSelector } from '@langchain/core/example_selectors';
import { AzureOpenAIEmbeddings, OpenAIEmbeddings } from '@langchain/openai';
import { NodeHtmlMarkdown } from 'node-html-markdown';
import { MemoryVectorStore } from 'langchain/vectorstores/memory';
import type { Critique } from '$lib/supabase';
import { formatXml } from '$lib/xml';
import {
	OPENAI_API_KEY,
	AZURE_OPENAI_API_KEY,
	AZURE_OPENAI_API_VERSION,
	AZURE_OPENAI_API_INSTANCE_NAME,
	AZURE_OPENAI_API_DEPLOYMENT_NAME,
} from '$env/static/private';

const embeddings = new OpenAIEmbeddings({ apiKey: OPENAI_API_KEY });

type Context = {
	name: string;
	content: string;
	index: number;
}[];

const formatOne = (critique: Critique) => {
	const output = NodeHtmlMarkdown.translate(critique.optimal);

	const queryItem = (critique.context as Context).at(-1)!;
	const query = `<${queryItem.name}>${NodeHtmlMarkdown.translate(queryItem.content)}</${queryItem.name}>`;

	let context: string[] = [];
	for (const contextItem of (critique.context as Context).slice(0, critique.context.length - 1)) {
		context = [
			...context,
			`<${contextItem.name}>${NodeHtmlMarkdown.translate(contextItem.content)}</${contextItem.name}>`,
		];
	}

	return {
		output: output,
		query: query,
		context: context.join('\n'),
	};
};

const formatCritiques = (critiques: Critique[]) => {
	const examples = critiques.map((critique: Critique) => formatOne(critique));

	return examples;
};

export const fewShotExampleMessages = async (critiques: Critique[], query: string) => {
	const examples = formatCritiques(critiques);
	console.log('examples', examples);

	const exampleSelector = await SemanticSimilarityExampleSelector.fromExamples(
		examples,
		embeddings,
		MemoryVectorStore,
		{
			k: 2,
		}
	);

	console.log('test1');
	const examplePrompt = PromptTemplate.fromTemplate(
		`<example><context>{context}</context><query>{query}</query><output>{output}</output></example>`
	);
	console.log('test2');

	const fewShotPrompt = new FewShotPromptTemplate({
		exampleSelector,
		examplePrompt,
		exampleSeparator: '',
		prefix: `<examples>`,
		suffix: '</examples>',
		inputVariables: ['query'],
	});
	console.log('test3');

	const formatval = await fewShotPrompt.format({ query: query });
	console.log('test4');

	console.log('xml input:\n', formatval);
	console.log('xml output:\n', await formatXml(formatval));
	return formatval;
};
