import {createSelector} from 'reselect'
import moment from 'moment';
import {groupBy, map} from 'lodash';

const timeslots = ( state ) => state.timeslots.list;
const selectedStore = ( state ) => 1;



export const getTimeslotsGroupedByDays = createSelector(
	[timeslots],
	( timeslots ) => {
		const foo = groupBy(timeslots, ( timeslot ) => {

			return moment(timeslot._timabil.hefst).startOf('day').toISOString();
		});

		return map(foo, (data, key) =>{
			return {
				date: moment(key).toDate(),
				data: map(data, (timeslot) => {
					const from = moment(timeslot._timabil.hefst).hour();
					const to = moment(timeslot._timabil.lykur).hour();

					return {
						id: timeslot.id,
						from: from,
						to: to,
						date: moment(key).toDate(),
						store: timeslot.starfsstod,
						needed: timeslot.lagmark,
						assigned: timeslot.skradir,
						max: timeslot.hamark
					}
				})
			}
		});
	}
)
