import {fetchTimeslotsForStore} from '../api/timeslotsApi';

export const getTimeSlotsForStore = (store) => ({
  type: 'GET_TIMESLOTS_FOR_STORE',
  payload: fetchTimeslotsForStore(store)
});
