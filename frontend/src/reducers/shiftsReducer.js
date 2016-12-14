import {fromJS, List, Map} from 'immutable';
import guid from '../utils/guid';
import moment from 'moment';
import {assign, filter, cloneDeep} from 'lodash';
import typeToReducer from 'type-to-reducer';
import {isSameDay, isEqual, isSameSecond, startOfDay, getHours, isBefore, isAfter, isWithinRange, setHours, setSeconds} from 'date-fns';

const defaultState = {
	list: [],
	loadingSkraning: false,
	vaktir: [],
	loaded: true
}

export default typeToReducer({
	'ADD_SHIFT': ( state, action ) => {
		let s = fromJS(state || {});
		let list = s.get('vaktir');
		if ( !list ) list = new List();

		const { to, from, date, store } = action.shift;

		const start = moment(date).hours(from);

		for ( let i = 0; i < to - from; i++ ) {
			list = list.push({
				hefst: start.toISOString(),
				lykur: start.hours(from + i + 1).toISOString(),
				starfsstod: { id: store }
			});
		}

		s = s.set('vaktir', list);
		return s.toJS();
	},
	'EDIT_SHIFT': ( state, action ) => {

		const { to, from, changeTo, changeFrom, date, location } = action.shift;

		let s = fromJS(state || {});
		let list = s.get('vaktir');

		list = list.filter(( vakt ) => {
			const isNotSameDate = !(isSameDay(vakt.get('hefst'), date));
			const start = getHours(vakt.get('hefst'));
			let end = getHours(vakt.get('lykur'));
			if ( end === 0 ) end = 24;
			const isSelected = changeFrom <= start && end <= changeTo;
			const hasNotBeenDeleted = !(from <= start && end <= to && !isSelected);

			return isNotSameDate || hasNotBeenDeleted;
		});

		if ( changeFrom < from ) {
			const start = moment(date).hours(changeFrom);

			for ( let i = changeFrom; i < from; i++ ) {
				list = list.push(Map({
					hefst: start.toISOString(),
					lykur: start.hours(i + 1).toISOString(),
					starfsstod: { id: location }
				}));
			}
		}

		if ( changeTo > to ) {
			const start = moment(date).hours(to);

			for ( let i = to; i < changeTo; i++ ) {
				list = list.push(Map({
					hefst: start.toISOString(),
					lykur: start.hours(i + 1).toISOString(),
					starfsstod: { id: location }
				}));
			}
		}

		/* CHANGE STORE IF NEEDED */
		const fromDate = setHours(date, changeFrom);
		const toDate = setHours(date, changeTo);

		list = list.map(( shift ) => {
			console.log('shift', shift);
			if ( isWithinRange(setSeconds(shift.get('hefst'), 1), fromDate, toDate) ) {
				shift = shift.set('starfsstod',  { id: location });
			}

			return shift;
		});

		console.log('foo', list.toJS());

		s = s.set('vaktir', list);
		return cloneDeep(s.toJS());
	},
	'DELETE_SHIFT': ( state, action ) => {
		const { to, from, date } = action.shift;
		let s = fromJS(state || {});
		let list = s.get('vaktir');

		list = list.filter(( vakt ) => {
			const isSameDate = moment(vakt.get('hefst')).isSame(date, 'day');
			const start = moment(vakt.get('hefst')).hour();
			const end = moment(vakt.get('lykur')).hour();
			const shouldBeDeleted = from <= start && end <= to;

			return !(isSameDate && shouldBeDeleted);
		});

		s = s.set('vaktir', list);
		return cloneDeep(s.toJS());
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
