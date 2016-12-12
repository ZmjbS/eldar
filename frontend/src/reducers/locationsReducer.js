import { assign, cloneDeep } from 'lodash';
import typeToReducer from 'type-to-reducer';

const defaultState = {
	list: [],
	loaded: true
};

export default typeToReducer({
	['LOAD_LOCATIONS']: {
		ERROR: ( state, action ) => {
			return cloneDeep(assign(state, {
				error: true,
			}))
		},
		SUCCESS: ( state, action ) => {
			return cloneDeep(assign(state, {
				list: action.payload.data,
			}))
		}
	}
}, defaultState);
