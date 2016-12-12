import { fetchAll } from '../api/locationsApi';

export const fetchLocations = () => ({
	type: 'LOAD_LOCATIONS',
	payload: fetchAll()
});
