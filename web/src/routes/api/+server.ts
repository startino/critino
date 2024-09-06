export const GET = async ({ locals: { supabase } }) => {
	const { data: critiqueIdsDict, error: eCritiqueIds } = await supabase
		.from('critiques')
		.select('id');

	if (!critiqueIdsDict || eCritiqueIds) {
		const message = `Error fetching critique IDs: ${JSON.stringify(eCritiqueIds, null, 2)}`;
		console.error(message);
		return new Response(JSON.stringify({ status: 500, message }), {
			headers: { 'Content-Type': 'application/json' },
		});
	}
	const critiqueIds = critiqueIdsDict.map((critique) => critique.id);

	return new Response(
		JSON.stringify({
			status: 200,
			message: 'Success',
			critiqueIds,
		}),
		{
			headers: { 'Content-Type': 'application/json' },
		}
	);
};
