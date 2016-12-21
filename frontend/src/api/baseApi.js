import axios from 'axios';
const instance = axios.create({
  baseURL: 'https://eldar.herokuapp.com/api',
 //baseURL: 'http://localhost:8000/api',
  //timeout: 4000
});

export default instance;
