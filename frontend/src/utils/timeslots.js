import find from 'lodash/find';

export const getTimeslotsForDate = ( list, date ) => find(list, { date: date }).data;

