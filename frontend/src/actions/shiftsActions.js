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

export const deleteShift = ( id ) => {
	return {
		type: 'DELETE_SHIFT',
		id
	}
}


