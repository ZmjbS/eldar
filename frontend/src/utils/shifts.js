import filter from 'lodash/filter';
import some from 'lodash/some';
import find from 'lodash/find';
import minBy from 'lodash/minBy';
import maxBy from 'lodash/maxBy';
import {getTimeslotsForDate} from './timeslots';

export const getTimeslot = ( timeslots, from ) => {
	return find(timeslots, { from: from });
}

export const isTimeslotFull = ( timeslots, from ) => {

	const timeslot = getTimeslot(timeslots, from);

	return !timeslot || timeslot.assigned >= timeslot.max; // Also sho full at the end of the day
}

export const hasShift = ( shifts, from ) => {
	return some(shifts, ( shift ) => {
		return shift.from <= from && from <= shift.from;
	})
}

export const getNextFullShift = ( timeslots, shifts, from, max ) => {
	for ( let i = from; i <= max; i++ ) {
		const isUnavailable = isTimeslotFull(timeslots, i + 1) || hasShift(shifts, i + 1);

		if ( isUnavailable ) {
			return i + 1;
		}
	}

	return max;
}

export const getPrevFullShift = ( timeslots, shifts, from, min ) => {
	for ( let i = from; i >= min; i-- ) {
		const isUnavailable = isTimeslotFull(timeslots, i - 1) || hasShift(shifts, i - 1);
		if ( isUnavailable ) {
			return i - 1;
		}
	}

	return min;
}

export const getShiftMinMax = ( timeslots, shifts, shift ) => {
	console.log('TIMESLOTS', timeslots);

	const timeslotsForDate = getTimeslotsForDate(timeslots, shift.date);
	const shiftsForDate = getTimeslotsForDate(shifts, shift.date);
	const maxTimeslot = maxBy(timeslotsForDate, 'from');
	const minTimeslot = minBy(timeslotsForDate, 'from');

	return {
		max: getNextFullShift(timeslotsForDate, shiftsForDate, shift.from, maxTimeslot.from),
		min: getPrevFullShift(timeslotsForDate, shiftsForDate, shift.from, minTimeslot.from) + 1
	}
}

export const getShiftsForDate = ( list, date ) => filter(list, { date: date });
