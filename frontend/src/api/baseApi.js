import axios from 'axios';
console.log('BASE URL', window.apiUrl);
const instance = axios.create({
  baseURL: 'https://eldar.herokuapp.com/api',
 //baseURL: 'http://localhost:8000/api',
  //timeout: 4000
});

export default instance;
