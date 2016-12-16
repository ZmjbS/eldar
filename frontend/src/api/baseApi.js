import axios from 'axios';
console.log('BASE URL', window.apiUrl);
const instance = axios.create({
  baseURL: 'https://eldar.herokuapp.com/api',
  timeout: 4000
});

export default instance;
