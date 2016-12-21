import baseApi from './baseApi';

export const fetchUserByEmail = ( email ) => {
	return baseApi.get('/felagi/', {
		params: {
			netfang: email.toLowerCase()
		}
	})
};

export const createOrUpdateUser = ( user ) => {
	const api = user.id ? baseApi.put : baseApi.post;

	return api(user.id ? '/felagi/' + user.id + '/' : '/felagi/', user)
}


