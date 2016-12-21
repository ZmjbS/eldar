'use strict';

import React, {PropTypes} from 'react';
import {connect} from 'react-redux'
import Box from '../Box/Box';
import {getUserByEmail} from '../../actions/userActions';
import {reset} from '../../actions/shiftsActions';
import styles from './Login.css';
/**
 * @class Login
 * @module *
 */
const mapStateToProps = ( state, props ) => {
	return {}
}

const mapDispatchToProps = ( dispatch ) => {
	return {
		onLogin: ( email ) => dispatch(getUserByEmail(email)),
		reset: () => dispatch(reset())
	}
}

class Login extends React.Component {

	componentDidMount = () => {
		this.props.reset();
	}

	onContinueClick = () => {
		this.props.onLogin(this.refs.email.value).then(() => {
			this.props.router.push('/user/create');
		})
	}

	render () {
		return (
			<Box>
				<h1 className={ styles.title }>HSSR</h1>
				<label className={ styles.label}>Tölvupóstfang</label>
				<input name="email" className={ styles.form} ref="email" />
				<button className={ styles.button } onClick={ this.onContinueClick }>Áfram</button>
			</Box>
		);
	}
}

export default connect(mapStateToProps, mapDispatchToProps)(Login);
