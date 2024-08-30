
export const load = async ({ cookies, locals: { user } }) => {
	const forms = {
	};

	return {
        user,
		forms,
		cookies: cookies.getAll(),
	};
};
