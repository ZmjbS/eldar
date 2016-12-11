import {saveShifts, fetchShiftsForUser} from '../api/shiftApi';

export const addShift = ( data ) => {
	return {
		type: 'ADD_SHIFT',
		shift: data
	}
}

export const editShift = ( data ) => {
	return {
		type: 'EDIT_SHIFT',
		shift: data
	}
}

export const deleteShift = ( shift ) => {
	return {
		type: 'DELETE_SHIFT',
		shift
	}
}

export const save = ( shiftIds, userId ) => ({
	type: 'SAVE_SHIFTS',
	payload: saveShifts(shiftIds, userId)
});


export const loadShifts = ( userId ) => ({
	type: 'LOAD_SHIFTS',
	payload: fetchShiftsForUser(userId)
});


