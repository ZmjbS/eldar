import map from 'lodash/map';
import random from 'lodash/random';

const getTimeslots = ( date, store ) => {
		return [
			{ id: 1, from: 10, to: 11, date: date, store: store, needed: 2, assigned: random(0, 3), max: 0 },
			{ id: 2, from: 11, to: 12, date: date, store: store, needed: 2, assigned: random(0, 3), max: 3 },
			{ id: 3, from: 12, to: 13, date: date, store: store, needed: 2, assigned: random(0, 3), max: 3 },
			{ id: 4, from: 13, to: 14, date: date, store: store, needed: 2, assigned: random(0, 3), max: 3 },
			{ id: 5, from: 14, to: 15, date: date, store: store, needed: 2, assigned: random(0, 3), max: 3 },
			{ id: 6, from: 15, to: 16, date: date, store: store, needed: 3, assigned: random(0, 3), max: 3 },
			{ id: 7, from: 16, to: 17, date: date, store: store, needed: 4, assigned: random(0, 3), max: 5 },
			{ id: 8, from: 17, to: 18, date: date, store: store, needed: 6, assigned: random(0, 7), max: 8 },
			{ id: 9, from: 18, to: 19, date: date, store: store, needed: 6, assigned: random(0, 7), max: 8 },
			{ id: 10, from: 19, to: 20, date: date, store: store, needed: 5, assigned: random(0, 7), max: 7 },
			{ id: 11, from: 20, to: 21, date: date, store: store, needed: 4, assigned: random(0, 4), max: 5 },
			{ id: 12, from: 21, to: 22, date: date, store: store, needed: 2, assigned: random(0, 2), max: 3 },
			{ id: 13, from: 22, to: 10, date: date, store: store, needed: 1, assigned: random(0, 2), max: 2, type: 'nightshift' },
		]
	};

const generateData = () => {
		const dates = [
			new Date(2016, 11, 27),
			new Date(2016, 11, 28),
			new Date(2016, 11, 29),
			new Date(2016, 11, 30),
			new Date(2016, 11, 31)
		];
		return map(dates, ( date ) => {
			return {
				date: date,
				data: getTimeslots(date, null)
			}
		})
	};


const defaultState = {
	list: generateData()
}

export default ( state = defaultState, action ) => {
	switch ( action.type ) {

		default:
			return state
	}
}
