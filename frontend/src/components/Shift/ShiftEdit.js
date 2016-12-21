import React, {PropTypes} from 'react';
import NumericInput from 'react-numeric-input';
import {connect} from 'react-redux'
import { map } from 'lodash';

import {editShift, deleteShift} from '../../actions/shiftsActions';
import {getShiftMinMax} from '../../utils/shifts';
import {getTimeslotsForDate} from '../../utils/timeslots';
import {getSelectedShifts} from '../../selectors/shiftsSelector';

import styles from './ShiftEdit.css'

const mapStateToProps = ( state, props ) => {
	return {
		...getShiftMinMax(props.timeslots, getSelectedShifts(state, props), props.shift),
		timeslots: getTimeslotsForDate(props.timeslots, props.date),
		locations: state.locations.list
	}
}

const mapDispatchToProps = ( dispatch ) => {
	return {
		onEditShift: ( shift ) => dispatch(editShift(shift)),
		onDeleteShift: ( id ) => dispatch(deleteShift(id))
	}
}

/**
 * @class ShiftEdit
 * @module *
 */
class ShiftEdit extends React.Component {

	//static defaultProps = {};
	//static propTypes = {};
	state = {
		from: this.props.shift.from,
		to: this.props.shift.to,
		location: this.props.shift.location.id
	};

	//componentWillMount () {}
	componentDidMount = () => {
		document.addEventListener('keydown', this.handleEscKey, false);
	}

	componentWillUnmount = () => {
		document.removeEventListener('keydown', this.handleEscKey, false);
	}
	//shouldComponentMount () { return true; }
	handleEscKey = ( event ) => {
		if ( event.keyCode == 27 ) {
			this.props.onClose();
		}
	}

	handleClickOutside = () => {
		if ( this.props.onClose )
			this.props.onClose();
	}

	onChangeFrom = ( value ) => {
		// TODO: VALIDATION

		this.setState({ from: value });
	}

	onChangeTo = ( value ) => {
		// TODO: VALIDATION

		this.setState({ to: value });
	}

	onChangeLocation = ( e ) => {
		// TODO: VALIDATION
		this.setState({ location: this.refs.location.value });
	}

	onChange = () => {

		if ( this.props.onEditShift )
			this.props.onEditShift({
				...this.props.shift,
				changeTo: this.state.to,
				changeFrom: this.state.from,
				location: this.state.location
			})

		this.props.onClose();
	}

	onDeleteTimeslot = ( from, to ) => {
		this.props.onDeleteShift();
	}

	handleDelete = () => {
		if ( this.props.onEditShift )
			this.props.onDeleteShift(this.props.shift);

		this.props.onClose();
	}

	stopClickThrough = ( e ) => {
		e.stopPropagation();
		return false;
	}

	render () {
		return (
			<div>
				<div className={ styles.overlay } onClick={ this.handleClickOutside }></div>
				<div className={ styles.editWrapper}>
					<div className={ styles.edit} onClick={ this.stopClickThrough }>
						<div className={ styles.formWrapper }>
							<label className={ styles.label }>Frá</label>
							<NumericInput className={ styles.form } value={ this.state.from } min={ this.props.min }
							              max={ this.state.to - 1 } onChange={ this.onChangeFrom } />
						</div>
						<div className={ styles.formWrapper }>
							<label className={ styles.label }>Til</label>
							<NumericInput className={ styles.form } value={ this.state.to } max={ this.props.max }
							              min={ this.state.from + 1 } onChange={ this.onChangeTo } />
						</div>
						<div className={ styles.formWrapper }>
							<label className={ styles.label }>Sölustaður</label>
							<select className={ styles.form } value={this.state.location} ref="location" onChange={ this.onChangeLocation }>
								{ map(this.props.locations, ( location ) => {
									return (<option key={ location.id } value={ location.id }>{location.nafn}</option>)
								})}
							</select>
						</div>
						<div className={ styles.buttonWrapper }>
							<button className={ styles.buttonDelete } onClick={ this.handleDelete }>Eyða</button>
							<button className={ styles.button} onClick={ this.onChange }>Staðfesta</button>
						</div>
					</div>
				</div>
			</div>);
	}
}

export default connect(mapStateToProps, mapDispatchToProps)(ShiftEdit);
