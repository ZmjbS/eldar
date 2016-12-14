import {fromJS, List} from 'immutable';
import map from 'lodash/map';
import random from 'lodash/random';
import typeToReducer from 'type-to-reducer';


const defaultState = {
	list: []
}


export default typeToReducer({
	['GET_TIMESLOTS_FOR_STORE']: {
		ERROR: ( state, action ) => ({
			isRejected: true,
			error: action.payload
		}),
		SUCCESS: ( state, action ) => {
			let s = fromJS(state || {});
			return s.set('list', action.payload.data).toJS();
		}
	}
}, defaultState);


