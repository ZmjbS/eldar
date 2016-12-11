import {createSelector} from 'reselect'
import moment from 'moment';
import {orderBy, groupBy, map, some, filter, find} from 'lodash';

const timeslots = ( state ) => state.timeslots.list;
const shifts = ( state ) => state.shifts.list;
const userShifts = ( state ) => {
	return state.shifts.vaktir ? state.shifts.vaktir : [];
}
const date = ( state, props ) => props.date;

export const getShiftsAsDateTime = createSelector([shifts], ( shifts ) => {
	return map(shifts, ( shift ) => {
		return {
			from: moment(shift.date).hours(shift.from),
			to: moment(shift.date).hours(shift.to),
		}
	})
})

export const getShiftsTimeslotIds = createSelector(
	[timeslots, userShifts],
	( timeslots, shifts ) => {

		const filtered = filter(timeslots, ( timeslot ) => {
			return some(shifts, ( shift ) => {
				return moment(shift.hefst).isSameOrBefore(timeslot._timabil.hefst) && moment(shift.lykur).isSameOrAfter(timeslot._timabil.lykur)
			})
		});

		return map(filtered, ( timeslot ) => {
			return timeslot.id;
		})
	}
)

const timeslotsForDate = createSelector([timeslots, date], ( timeslots, date ) => {
	return filter(timeslots, ( timeslot ) => {
		return moment(timeslot._timabil.hefst).isSame(date, 'day')
	});
});

const shiftsForDate = createSelector([shifts, date], ( shifts, date ) => {
	return filter(shifts, { date: date });
});

const vaktirForDate = createSelector([userShifts, date], ( userShifts, date ) => {
	return orderBy(filter(userShifts, ( shift ) => (moment(shift.hefst).isSame(date, 'day'))), 'hefst');
});

export const getSelectedShifts = createSelector([timeslotsForDate, vaktirForDate], ( timeslots, vaktirForDate ) => {

	if ( vaktirForDate.length === 0 ) return [];

	let shifts2 = [];
	let start = moment(vaktirForDate[0].hefst).hour();
	let end = moment(vaktirForDate[vaktirForDate.length - 1].lykur).hour();

	console.log('v', vaktirForDate);

	map(timeslots, (timeslot) => {
		const s = moment(timeslot._timabil.hefst);
		const l = moment(timeslot._timabil.lykur);

		const f = find(vaktirForDate, { hefst: timeslot._timabil.hefst})

		if(!!f)
			console.log('f', f);

	})


	//
	// map(vaktirForDate, ( vakt ) => {
	// 	const timeslot = find(timeslots, ( timeslot ) => {
	// 		return moment(timeslot._timabil.hefst).isSame(date)
	// 	});
	//
	// 	console.log('t', timeslot, vakt);
	//
	// })

	// for(let i = 1; i < vaktirForDate.length; i++){
	// 	const prev = vaktirForDate[i-1];
	// 	const d = vaktirForDate[i];
	// 	const next = vaktirForDate[i+1];
	//
	// 	if(!next){
	// 		shifts2.push({
	// 			from: moment(start).hour(),
	// 			to: moment(d.lykur).hour(),
	// 			date: moment(start).startOf('day').toDate()
	// 		})
	// 	} else if(d.hefst === prev.lykur){
	//
	// 	} else {
	// 		shifts2.push({
	// 			from: moment(start).hour(),
	// 			to: moment(prev.lykur).hour(),
	// 			date: moment(start).startOf('day').toDate()
	// 		});
	//
	// 		if(next)
	// 			start = next.hefst
	// 	}
	// }

	console.log('ss', shifts2);
	return shifts2;

})
