import { combineReducers } from 'redux'
import shifts from './shiftsReducer'
import timeslots from './timeslotsReducer'

const app = combineReducers({
  shifts,
  timeslots
})

export default app
