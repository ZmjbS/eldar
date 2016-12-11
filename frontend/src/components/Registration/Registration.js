'use strict';

import React, {PropTypes} from 'react';
import {connect} from 'react-redux'
import merge from 'lodash/merge';
import Box from '../Box/Box';
import {saveUser} from '../../actions/userActions';
import styles from '../Login/Login.css';

/**
 * @class Registration
 * @module *
 */
const mapStateToProps = ( state, props ) => {
	return {
		currentUser: state.users.currentUser || {}
	}
}

const mapDispatchToProps = ( dispatch ) => {
	return {
		onSaveUser: ( user ) => dispatch(saveUser(user)),
	}
}

class Registration extends React.Component {

	//static defaultProps = {};
	//static propTypes = {};
	state = {
		name: this.props.currentUser.nafn,
		phone: this.props.currentUser.simi
	};

	componentWillMount = () => {
		if(!this.props.currentUser.netfang)
			this.props.router.push('/');
	}
	//componentDidMount () {}
	//componentWillUnmount () {}
	//shouldComponentMount () { return true; }

	componentWillReceiveProps = ( nextProps ) => {
		if ( nextProps.currentUser !== this.props.currentUser ) {
			this.setState({
				name: nextProps.currentUser.nafn,
				phone: nextProps.currentUser.simi
			})
		}
	}

	onContinueClick = () => {
		const { currentUser } = this.props;
		const { name, phone } = this.refs;

		this.props.onSaveUser(merge(currentUser, {
			nafn: name.value,
			simi: phone.value
		})).then(() => {
			this.props.router.push('/user/' + currentUser.netfang);
		});

	}

	handleChange = () => {
		const { name, phone } = this.refs;
		this.setState({
			name: name.value,
			phone: phone.value
		});
	}

	render () {
		console.log('state', this.state);
		console.log('props', this.props);
		const { name, phone } = this.state;

		return (
			<Box>
				<h1 className={ styles.title }>Skráning</h1>
				<div className={ styles.subTitle}>Okkur vantar eftirfarandi upplýsingar til að geta haldið áfram</div>
				<label className={ styles.label }>Nafn</label>
				<input className={ styles.form } value={name || ''} ref="name" onChange={ this.handleChange } />
				<label className={ styles.label }>Símanúmer</label>
				<input className={ styles.form } value={phone || ''} ref="phone" onChange={ this.handleChange } />
				<button className={ styles.button } onClick={ this.onContinueClick }>Áfram</button>

			</Box>
		);
	}
}

export default connect(mapStateToProps, mapDispatchToProps)(Registration);
