export const POST = async ({ request }) => {
	const data = await request.json();

	console.log(JSON.stringify(data, null, 2));

	return new Response(JSON.stringify({ message: 'Hello', data }), {
		headers: { 'Content-Type': 'application/json' },
	});
};
