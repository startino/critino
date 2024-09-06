import { PUBLIC_SITE_URL } from '$env/static/public';
import { getURL } from '$lib/utils.js';

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
		return new Response(JSON.stringify({ status: 500, message }), {
			headers: { 'Content-Type': 'application/json' },
		});
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
		return new Response(JSON.stringify({ status: 500, message }), {
			headers: { 'Content-Type': 'application/json' },
		});
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
		return new Response(JSON.stringify({ status: 500, message }), {
			headers: { 'Content-Type': 'application/json' },
		});
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
		return new Response(JSON.stringify({ status: 500, message }), {
			headers: { 'Content-Type': 'application/json' },
		});
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
		return new Response(JSON.stringify({ status: 500, message }), {
			headers: { 'Content-Type': 'application/json' },
		});
	}

	console.log(JSON.stringify(critique, null, 2));

	return new Response(
		JSON.stringify({
			status: 200,
			message: 'Success',
			critique,
			redirect_url: `${getURL()}projects/${project.name}/workflows/${workflow.name}/critiques/${critique.id}`,
		}),
		{
			headers: { 'Content-Type': 'application/json' },
		}
	);
};
