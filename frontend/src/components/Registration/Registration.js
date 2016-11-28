'use strict';

import React, {PropTypes} from 'react';
import Box from '../Box/Box';
import styles from '../Login/Login.css';
/**
 * @class Registration
 * @module *
 */
class Registration extends React.Component {

	//static defaultProps = {};
	//static propTypes = {};
	//state = {};

	//componentWillMount () {}
	//componentDidMount () {}
	//componentWillUnmount () {}
	//shouldComponentMount () { return true; }

	onContinueClick = () => {
		this.props.router.push('/user/baldurarna@gmail.com');
	}

	render () {
		return (
			<Box>
				<h1 className={ styles.title }>Skráning</h1>
				<div className={ styles.subTitle}>Okkur vantar eftirfarandi upplýsingar til að geta haldið áfram</div>
				<label className={ styles.label }>Nafn</label>
				<input  className={ styles.form } />
				<label className={ styles.label }>Símanúmer</label>
				<input  className={ styles.form }/>
				<button className={ styles.button } onClick={ this.onContinueClick }>Áfram</button>

			</Box>
		);
	}
}

export default Registration;
