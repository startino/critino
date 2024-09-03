export const POST = async ({ request, locals: { supabase } }) => {
	const data = await request.json();

	console.log(JSON.stringify(data, null, 2));

	return data;
};
