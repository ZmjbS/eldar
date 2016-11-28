'use strict';

import React, {PropTypes} from 'react';
import Box from '../Box/Box';
import styles from './Login.css';
/**
 * @class Login
 * @module *
 */
class Login extends React.Component {

	onContinueClick = () => {
		console.log(this.props);
		this.props.router.push('/user/create');
	}

	render () {
		return (
			<Box>
				<h1 className={ styles.title }>HSSR</h1>
				<label className={ styles.label}>Tölvupóstfang</label>
				<input name="email" className={ styles.form} />
				<button className={ styles.button } onClick={ this.onContinueClick }>Áfram</button>
			</Box>
		);
	}
}

export default Login;
