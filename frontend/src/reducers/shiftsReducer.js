import {fromJS} from 'immutable';
import guid from '../utils/guid';

const defaultState = {
	list: []
}

export default ( state = defaultState, action ) => {
	let list = fromJS(state.list);

	switch ( action.type ) {
		case 'ADD_SHIFT':
			list = list.push({
				id: guid(),
				...action.shift
			});

			return {
				list: list.toJS()
			};

		case 'EDIT_SHIFT':
			const shift = action.shift;

			list = list.update(
				list.findIndex(function ( item ) {
					return item.get('id') === shift.id;
				}), function ( item ) {
					item = item.set('from', shift.from);
					item = item.set('to', shift.to);
					item = item.set('date', shift.date);
					// TODO: STORE
					return item;
				}
			);
			return {
				list: list.toJS()
			};

		case 'DELETE_SHIFT':
			console.log('DELETE', action);
			list = list.filter(( item ) => {
				return item.get('id') !== action.id;
			});

			return {
				list: list.toJS()
			};
		default:
			return state
	}
}
