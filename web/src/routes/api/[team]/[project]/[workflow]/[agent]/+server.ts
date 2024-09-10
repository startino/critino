import { getURL } from '$lib/utils.js';
import { fewShotExampleMessages } from './fewShot';
import { NodeHtmlMarkdown } from 'node-html-markdown';

export const GET = async ({ params, request, locals: { supabase } }) => {
	if (request.headers.get('Content-Length')) {
		const data = await request.json();
	}

	let { data: critiques, error: eCritiques } = await supabase
		.from('critiques')
		.select()
		.eq('team_name', params.team)
		.eq('project_name', params.project)
		.eq('workflow_name', params.workflow)
		.eq('agent_name', params.agent);

	if (!critiques || eCritiques) {
		const message = `Error fetching critiques: ${JSON.stringify(eCritiques, null, 2)}`;
		console.error(message);
		return Response.json({ status: 500, message });
	}

	critiques = critiques.filter(
		(critique) =>
			critique.optimal &&
			critique.optimal.trim() !== '' &&
			critique.optimal.trim() !== '<p></p>'
	);

	const message = fewShotExampleMessages(critiques, `<user>hello</user>`);

	critiques.map((critique) => {
		critique.optimal = NodeHtmlMarkdown.translate(critique.optimal);
		critique.context.map((context) => {
			context.content = NodeHtmlMarkdown.translate(context.content);
		});
	});

	return Response.json({
		status: 200,
		message,
		critiques: critiques.map(({ context, optimal }) => ({ context, optimal })),
	});
};

export const POST = async ({ params, request, locals: { supabase } }) => {
	const data = await request.json();

	const { data: team, error: eTeam } = await supabase
		.from('teams')
		.select()
		.eq('name', params.team)
		.single();

	if (!team || eTeam) {
		const message = `Error fetching team: ${JSON.stringify(eTeam, null, 2)}`;
		console.error(message);
		return Response.json({ status: 500, message });
	}

	const { data: project, error: eProject } = await supabase
		.from('projects')
		.select()
		.eq('team_name', params.team)
		.eq('name', params.project)
		.single();

	if (!project || eProject) {
		const message = `Error fetching project: ${JSON.stringify(eProject, null, 2)}`;
		console.error(message);
		return Response.json({ status: 500, message });
	}

	const { data: workflow, error: eWorkflow } = await supabase
		.from('workflows')
		.upsert({
			team_name: params.team,
			project_name: params.project,
			name: params.workflow,
		})
		.select()
		.single();

	if (!workflow || eWorkflow) {
		const message = `Error creating workflow: ${JSON.stringify(eWorkflow, null, 2)}`;
		console.error(message);
		return Response.json({ status: 500, message });
	}

	const { error: eAgent } = await supabase
		.from('agents')
		.upsert({
			team_name: params.team,
			project_name: params.project,
			workflow_name: params.workflow,
			name: params.agent,
		})
		.select()
		.single();

	if (eAgent) {
		const message = `Error creating agent: ${JSON.stringify(eAgent, null, 2)}`;
		console.error(message);
		return Response.json({ status: 500, message });
	}

	const { data: critique, error: eCritique } = await supabase
		.from('critiques')
		.insert({
			team_name: params.team,
			project_name: params.project,
			workflow_name: params.workflow,
			agent_name: params.agent,
			...data,
		})
		.select()
		.single();

	if (!critique || eCritique) {
		const message = `Error creating critique: ${JSON.stringify(eCritique, null, 2)}`;
		console.error(message);

		return Response.json({ status: 500, message });
	}

	console.log(JSON.stringify(critique, null, 2));

	return Response.json({
		status: 200,
		message: 'Success',
		critique,
		redirect_url: `${getURL()}projects/${project.name}/workflows/${workflow.name}/critiques/${critique.id}`,
	});
};
