import baseApi from './baseApi';

export const fetchTimeslotsForStore = ( storeId ) => {
	return baseApi.get('/vakt/', {
		params: {
			starfsstod: storeId
		}
	})
};
