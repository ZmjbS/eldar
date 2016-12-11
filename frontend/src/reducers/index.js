import {combineReducers} from 'redux'
import shifts from './shiftsReducer'
import timeslots from './timeslotsReducer'
import users from './userReducer'

const app = combineReducers({
	shifts,
	timeslots,
	users
})

export default app
