import typeToReducer from 'type-to-reducer';
import {fromJS, List} from 'immutable';

export default typeToReducer({
	['GET_USER_BY_EMAIL']: {
		PENDING: () => ({
			// ...

		}),
		ERROR: ( state, action ) => ({
			isRejected: true,
			error: action.payload
		}),
		SUCCESS: ( state, action ) => {
			const data = action.payload.data;

			const s = fromJS(state);
			return s.set('currentUser', data && data.length > 0 ?
				data[0] :
				{ netfang: action.payload.config.params.netfang }).toJS();

		}
	},
	['SAVE_USER']: {
		PENDING: () => ({
			// ...

		}),
		ERROR: ( state, action ) => ({
			isRejected: true,
			error: action.payload
		}),
		SUCCESS: ( state, action ) => {
			const data = action.payload.data;
			const s = fromJS(state);
			return s.set('currentUser', data).toJS();
		}
	}
}, {
	currentUser: null
});
