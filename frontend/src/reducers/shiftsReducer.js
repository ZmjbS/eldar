import {fromJS} from 'immutable';
import guid from '../utils/guid';
import moment from 'moment';
import {assign, filter} from 'lodash';
import cloneDeep from 'lodash/cloneDeep';
import typeToReducer from 'type-to-reducer';

const defaultState = {
	list: [],
	loadingSkraning: false,
	vaktir: [],
	loaded: true
}

export default typeToReducer({
	'ADD_SHIFT': ( state, action ) => {
		let list = fromJS(state.vaktir || []);
		const { to, from } = action.shift;

		const start = moment(action.shift.date).hours(from);

		for ( let i = 0; i < to - from; i++ ) {
			list = list.push({
				_id: guid(),
				hefst: start.toISOString(),
				lykur: start.hours(from + i + 1).toISOString(),
			});
		}

		return cloneDeep(assign(state, {
			vaktir: (list.toJS())
		}));
	},
	'EDIT_SHIFT': ( state, action ) => {

		const { to, from, changeTo, changeFrom, date } = action.shift;

		let list = fromJS(state.vaktir || []);

		list = list.filter(( vakt ) => {
			const isNotSameDate = !(moment(vakt.get('hefst')).isSame(date, 'day'));
			const start = moment(vakt.get('hefst')).hour();
			const end = moment(vakt.get('lykur')).hour();
			const isSelected = changeFrom <= start && end <= changeTo;
			const hasNotBeenDeleted = !(from <= start && end <= to && !isSelected);

			console.log('DELETE', start, end, isNotSameDate, isSelected, hasNotBeenDeleted);

			return isNotSameDate || hasNotBeenDeleted;
		});

		if ( changeFrom < from ) {
			const start = moment(date).hours(changeFrom);
			console.log('START', start, from, changeFrom);

			for ( let i = changeFrom; i < from; i++ ) {
				const foo = {
					_id: guid(),
					hefst: start.toISOString(),
					lykur: start.hours(i + 1).toISOString(),
				}
				console.log('i', i, foo);
				list = list.push(foo);
			}
		}

		if ( changeTo > to ) {
			const start = moment(date).hours(to);
			console.log('END', start, to, changeTo);

			for ( let i = to; i < changeTo; i++ ) {
				const foo = {
					_id: guid(),
					hefst: start.toISOString(),
					lykur: start.hours(i + 1).toISOString(),
				}
				console.log('i', i, foo);
				list = list.push(foo);
			}
		}

		return cloneDeep(assign(state, {
			vaktir: list.toJS()
		}));
	},
	'DELETE_SHIFT': ( state, action ) => {
		const { to, from, date } = action.shift;
		let list = fromJS(state.vaktir || []);

		list = list.filter(( vakt ) => {
			const isSameDate = moment(vakt.get('hefst')).isSame(date, 'day');
			const start = moment(vakt.get('hefst')).hour();
			const end = moment(vakt.get('lykur')).hour();
			const shouldBeDeleted = from <= start && end <= to;

			console.log('shouldBeDeleted', shouldBeDeleted, from, start, end, to);

			return !(isSameDate && shouldBeDeleted);
		});

		return cloneDeep(assign(state, {
			vaktir: list.toJS()
		}));
	},
	['LOAD_SHIFTS']: {
		PENDING: ( state ) => (cloneDeep(assign(state, {
			loadingSkraning: true
		}))),
		ERROR: ( state, action ) => {
			return cloneDeep(assign(state, {
				error: true,
				loadingSkraning: false
			}))
		},
		SUCCESS: ( state, action ) => {
			return cloneDeep(assign(state, {
				skraning: action.payload.data,
				vaktir: action.payload.data._vaktir,
				loadingSkraning: false,
				loaded: true
			}))
		}
	}
}, defaultState);
