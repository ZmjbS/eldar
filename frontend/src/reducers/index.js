import {combineReducers} from 'redux'
import shifts from './shiftsReducer'
import timeslots from './timeslotsReducer'
import users from './userReducer'
import locations from './locationsReducer'

const app = combineReducers({
	shifts,
	timeslots,
	users,
	locations
})

export default app
