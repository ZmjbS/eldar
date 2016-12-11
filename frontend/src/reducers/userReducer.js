import typeToReducer from 'type-to-reducer';

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

			return {
				currentUser: data && data.length > 0 ?
					data[0] :
					{ netfang: action.payload.config.params.netfang }
			}
		}
	}
}, {
	currentUser: null
});
