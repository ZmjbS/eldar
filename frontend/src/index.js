import React from 'react';
import ReactDOM from 'react-dom';
import {Router, Route, withRouter, browserHistory} from 'react-router'
import {Provider} from 'react-redux'
import {createStore, combineReducers} from 'redux'
import reducer from './reducers/index'
import App from './components/App/App';
import Registration from './components/Registration/Registration';
import Login from './components/Login/Login'

let store = createStore(reducer);

ReactDOM.render(
	<Provider store={store}>
		<Router history={browserHistory}>
			<Route path="/" component={ withRouter(Login) } />
			<Route path="/user/create" component={ withRouter(Registration) } />
			<Route path="/user/:email" component={ withRouter(App) } />
		</Router>
	</Provider>
	,document.getElementById('root'));
