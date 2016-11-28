import React, {PropTypes} from 'react';
import NumericInput from 'react-numeric-input';
import {connect} from 'react-redux'

import {editShift, deleteShift} from '../../actions/shiftsActions';
import {getShiftMinMax} from '../../utils/shifts';

import styles from './ShiftEdit.css'

const mapStateToProps = ( state, props ) => {
	return {
		...getShiftMinMax(state.timeslots.list, state.shifts.list, props.shift),
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
		to: this.props.shift.to
	};

	//componentWillMount () {}
	//componentDidMount () {}
	//componentWillUnmount () {}
	//shouldComponentMount () { return true; }

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

	onChange = () => {
		if ( this.props.onEditShift )
			this.props.onEditShift({
				...this.props.shift,
				to: this.state.to,
				from: this.state.from,
			})

		this.props.onClose();
	}

	handleDelete = () => {
		if ( this.props.onEditShift )
			this.props.onDeleteShift(this.props.shift.id);

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
