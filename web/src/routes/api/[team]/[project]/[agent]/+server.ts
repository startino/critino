export const POST = async ({ params, request, locals: { supabase } }) => {
	const data = await request.json();

	const { data: critique, error: eCritique } = await supabase
		.from('critiques')
		.insert({
			team_name: params.team,
			project_name: params.project,
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

	return new Response(JSON.stringify({ status: 200, message: 'Success', critique }), {
		headers: { 'Content-Type': 'application/json' },
	});
};
