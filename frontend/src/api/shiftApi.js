import baseApi from './baseApi';

export const fetchShiftsForUser = ( userId ) => {
	return baseApi.get('/skraning/', {
		params: {
			felagi: userId
		}
	})
};

export const saveShifts = (shiftIds, userId) => {
	return baseApi.post('/skraning/', {
		athugasemd: '',
		felagi: userId,
		vaktir: shiftIds
	});
}

