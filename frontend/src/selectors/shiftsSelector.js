import {createSelector} from 'reselect'
import moment from 'moment';
import {orderBy, groupBy, map, some, filter, find, flatten} from 'lodash';
import {isSameDay, isEqual, isSameSecond, startOfDay, getHours, isBefore, isAfter} from 'date-fns';

const timeslots = ( state ) => state.timeslots.list;
const shifts = ( state ) => state.shifts.list;
const locations = ( state ) => state.locations.list;
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

const getSimpleTimeslots = createSelector([timeslots], ( timeslots ) => {
	return map(timeslots, ( timeslot ) => {
		return {
			id: timeslot.id,
			hefst: timeslot.hefst,
			lykur: timeslot.lykur,
			starfsstod: timeslot.starfsstod
		}
	})
});

const getSimpleTimeslotsGroupedByStore = createSelector([getSimpleTimeslots], ( timeslots ) => {
	return groupBy(timeslots, 'starfsstod');
});

const getUserShiftsGroupedByStore = createSelector([userShifts], ( shifts ) => {
	return groupBy(shifts, 'starfsstod.id')
});

const getShiftsTimeslotIdsForShifts = ( timeslots, shifts ) => {
	const s = map(shifts, ( shift ) => {
		return {
			hefst: moment(shift.hefst),
			lykur: moment(shift.lykur)
		}
	});

	const filtered = filter(timeslots, ( timeslot ) => {
		return some(s, ( shift ) => {
			// return (isEqual(timeslot.hefst, shift.hefst) || isBefore(timeslot.hefst, shift.hefst))
			// 	&& (isEqual(timeslot.lykur, shift.lykur) || isAfter(timeslot.lykur, shift.lykur));
			return shift.hefst.isSameOrBefore(timeslot.hefst) && shift.lykur.isSameOrAfter(timeslot.lykur)
		})
	});

	return map(filtered, ( timeslot ) => {
		return timeslot.id;
	})
}

export const getShiftsTimeslotIds = createSelector(
	[getSimpleTimeslotsGroupedByStore, getUserShiftsGroupedByStore],
	( timeslots, shiftsByDays ) => {

		const ids = flatten(map(shiftsByDays, ( shifts, key ) => (getShiftsTimeslotIdsForShifts(timeslots[key], shifts))));

		return ids;
	}
)

const timeslotsForDate = createSelector([timeslots, date], ( timeslots, date ) => {
	return filter(timeslots, ( timeslot ) => {
		return moment(timeslot.hefst).isSame(date, 'day')
	});
});

const shiftsForDate = createSelector([shifts, date], ( shifts, date ) => {
	return filter(shifts, { date: date });
});

const vaktirForDate = createSelector([userShifts, date], ( userShifts, date ) => {
	return orderBy(filter(userShifts, ( shift ) => (moment(shift.hefst).isSame(date, 'day'))), 'hefst');
});

const getSelectedShiftsForTimeslots = ( timeslots, shifts, locations ) => {

	if ( shifts.length === 0 ) return [];

	let shifts2 = [];

	const vaktirHefst = map(shifts, ( shift ) => (shift.hefst))

	for ( let t = 0; t < timeslots.length; t++ ) {
		const startTimeslot = timeslots[t];

		if ( !some(vaktirHefst, ( vakt ) => (isSameSecond(vakt, startTimeslot.hefst))) ) continue;

		while ( !!timeslots[t + 1] && some(vaktirHefst, ( vakt ) => (isSameSecond(vakt, timeslots[t + 1].hefst))) && isSameDay(timeslots[t+1].hefst, startTimeslot.hefst)) {
			t++;
		}

		const endTimeslot = timeslots[t];

		const to = getHours(endTimeslot.lykur);

		const location = find(locations, { id: startTimeslot.starfsstod });

		shifts2.push({
			from: getHours(startTimeslot.hefst),
			to: to === 0 ? 24 : to,
			date: startOfDay(startTimeslot.hefst),
			location: location
		});

	}

	return shifts2;
}

export const getSelectedShifts = createSelector([getSimpleTimeslotsGroupedByStore, getUserShiftsGroupedByStore, locations], ( timeslots, shiftsByDays, locations ) => {
	return flatten(map(shiftsByDays, (shifts, key) => (getSelectedShiftsForTimeslots(timeslots[key], shifts, locations))));
})

export const getSelectedShiftsForDate = createSelector([date, getSelectedShifts], ( date, shifts ) => {
	return filter(shifts, ( shift ) => {
		return moment(shift.date).isSame(date, 'day');
	})
})
