import React from 'react';
import ReactDOM from 'react-dom';
import {Router, Route, withRouter, browserHistory} from 'react-router'
import {Provider} from 'react-redux'
import {createStore, combineReducers, applyMiddleware} from 'redux'
import reducer from './reducers/index'
import App from './components/App/App';
import Registration from './components/Registration/Registration';
import Login from './components/Login/Login'
import promiseMiddleware from 'redux-promise-middleware';
import endsWith from 'lodash/endsWith'

const middleware = [];

middleware.push(promiseMiddleware({
	promiseTypeSuffixes: ['PENDING', 'SUCCESS', 'ERROR']
}));

if ( process.env.NODE_ENV !== 'production' ) {
	middleware.push(require('redux-logger')({
		colors: {
			title: ( { type } ) => {
				if ( endsWith(type, 'SUCCESS') ) {
					return 'MEDIUMSEAGREEN'
				} else if ( endsWith(type, 'PENDING') ) {
					return 'DARKGRAY'
					// return 'STEELBLUE'
				} else if ( endsWith(type, 'ERROR') ) {
					return 'CRIMSON'
				} else {
					return 'MEDIUMSEAGREEN'
					// return 'DARKGRAY'
				}
			}
		},
		timestamp: false,
		// diff: true,
		collapsed: true,
		duration: true
	}))
}

let store = createStore(reducer, applyMiddleware(...middleware));



ReactDOM.render(
	<Provider store={store}>
		<Router history={browserHistory}>
			<Route path="/" component={ withRouter(Login) } />
			<Route path="/user/create" component={ withRouter(Registration) } />
			<Route path="/user/:email" component={ withRouter(App) } />
		</Router>
	</Provider>
	, document.getElementById('root'));
