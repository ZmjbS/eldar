import {fetchUserByEmail, createOrUpdateUser} from '../api/userApi';

export const getUserByEmail = (email) => ({
  type: 'GET_USER_BY_EMAIL',
  payload: fetchUserByEmail(email)
});


export const saveUser = (user) => ({
  type: 'SAVE_USER',
  payload: createOrUpdateUser(user)
});
