'use strict';

import React, {PropTypes} from 'react';
import {connect} from 'react-redux'
import {merge, map} from 'lodash';
import Box from '../Box/Box';
import {saveUser} from '../../actions/userActions';
import {fetchLocations} from '../../actions/locationsActions';
import styles from '../Login/Login.css';

/**
 * @class Registration
 * @module *
 */
const mapStateToProps = ( state, props ) => {
	return {
		currentUser: state.users.currentUser || {},
		locations: state.locations.list
	}
}

const mapDispatchToProps = ( dispatch ) => {
	return {
		onSaveUser: ( user ) => dispatch(saveUser(user)),
		loadLocations: ( ) => dispatch(fetchLocations())
	}
}

class Registration extends React.Component {

	//static defaultProps = {};
	//static propTypes = {};
	state = {
		name: this.props.currentUser.nafn,
		phone: this.props.currentUser.simi,
		location: this.props.currentUser.adalStarfsstod
	};

	componentWillMount = () => {
		if ( !this.props.currentUser.netfang )
			this.props.router.push('/');

		if(this.props.locations.length === 0){
			this.props.loadLocations();
		}
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
		const { name, phone, location } = this.refs;

		this.props.onSaveUser(merge(currentUser, {
			nafn: name.value,
			simi: phone.value,
			adalStarfsstod: location.value
		})).then(() => {
			this.props.router.push('/user/' + currentUser.netfang);
		});

	}

	handleChange = () => {
		const { name, phone, location } = this.refs;
		this.setState({
			name: name.value,
			phone: phone.value,
			location: location.value
		});
	}

	render () {
		const { name, phone, location } = this.state;

		return (
			<Box>
				<h1 className={ styles.title }>Skráning</h1>
				<div className={ styles.subTitle}>Okkur vantar eftirfarandi upplýsingar til að geta haldið áfram</div>
				<label className={ styles.label }>Nafn</label>
				<input className={ styles.form } value={name || ''} ref="name" onChange={ this.handleChange } />
				<label className={ styles.label }>Símanúmer</label>
				<input className={ styles.form } value={phone || ''} ref="phone" onChange={ this.handleChange } />
				<label className={ styles.label }>Aðal sölustaður</label>
				<select className={ styles.form } value={location} ref="location" onChange={ this.handleChange }  >
					{ map(this.props.locations, (location) => {
						return (<option key={ location.id } value={ location.id }>{location.nafn}</option>)
					})}

				</select>
				<button className={ styles.button } onClick={ this.onContinueClick }>Áfram</button>

			</Box>
		);
	}
}

export default connect(mapStateToProps, mapDispatchToProps)(Registration);
