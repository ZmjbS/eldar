import React, {PropTypes} from 'react';
import moment from 'moment';
import map from 'lodash/map';
import minBy from 'lodash/minBy';
import chroma from 'chroma-js';
import InlineSVG from 'svg-inline-react';
import {connect} from 'react-redux'
import { getShiftsForDate, getNextFullShift, isTimeslotFull } from '../../utils/shifts';
import { getTimeslotsForDate } from '../../utils/timeslots';

import {getSelectedShifts} from '../../selectors/shiftsSelector';

import Shift from '../Shift/Shift';

import {addShift} from '../../actions/shiftsActions';

import BackIcon from './back.svg'
import NextIcon from './next.svg'

import styles from './CalanderDate.css';



const mapStateToProps = ( state, props ) => {
	return {
		shifts: getSelectedShifts(state, props),
		timeslots: getTimeslotsForDate(props.timeslots, props.date)
	}
}

const mapDispatchToProps = ( dispatch ) => {
	return {
		onAddShift: ( shift ) => dispatch(addShift(shift))
	}
}

/**
 * @class Date
 * @module *
 */
class CalanderDate extends React.Component {

	static defaultProps = {
		defaultShiftLength: 4
	};

	static propTypes = {
		defaultShiftLength: PropTypes.number
	};

	state = {
		shifts: []
	};



	addShift = ( from ) => {
		return () => {

			if ( isTimeslotFull(this.props.timeslots, from) ) {
				// TODO: add message to tell that the shift is full
				console.log('FULL');
				return;
			}

			this.props.onAddShift({
				from: from,
				to: getNextFullShift(this.props.timeslots, this.props.shifts, from, from + this.props.defaultShiftLength),
				date: this.props.date
			});
		}
	};

	timeToPixels = ( time ) => {
		const min = minBy(this.props.timeslots, 'from');

		return (time - min.from) * 30;
	};

	hoursToPixels = ( hours ) => {
		return hours * 30;
	};

	getSlotColorStyle = ( slot ) => {
		const scale = chroma.scale(['#ffffff', '#60B294']).classes([0, 0.3, 0.6, 0.7, 0.8, 1]);

		if ( slot.max === 0 ) {
			return {
				background: 'repeating-linear-gradient(45deg,#B0BABF,#B0BABF 15px,#C3CDD4 15px,#C3CDD4 30px)',
				opacity: 0.7
			}
		}

		if ( slot.assigned >= slot.max ) {
			return {
				background: 'repeating-linear-gradient(45deg,#50947B,#50947B 15px,#60B294 15px,#60B294 30px)',
				opacity: 0.7
			}
		}

		if ( !this.props.showShiftBackground )
			return {};

		return {
			backgroundColor: scale(slot.assigned / slot.needed),
			opacity: 0.7
		}
	};

	handleChange = ( data ) => {
		this.props.onChange(data, this.props.date)
	}

	renderHead = () => {
		const dateFormated = moment(this.props.date).format('ddd DD.MM');

		if ( window.innerWidth > 400 ) {
			return (<div className={ styles.head }>{ dateFormated }</div>);
		}

		return (
			<div className={ styles.head }>
				<span onClick={ this.props.onPrevDay } className={ styles.icon }>
					<InlineSVG src={ BackIcon } />
				</span>
				<span className={ styles.day }>{ dateFormated }</span>
				<span onClick={ this.props.onNextDay } className={ styles.icon }>
					<InlineSVG src={ NextIcon } />
				</span>
			</div>
		);
	}

	render = () => {
		const { timeslots, shifts } = this.props;



		return (
			<div className={ [styles.main, this.props.className].join(' ') }>
				{ this.renderHead() }
				<div className={ styles.shiftsWrapper } style={ { height: timeslots.length * 30 }}>
					<div className={ styles.shifts }>
						{ map(shifts, ( shift ) => {
							const style = {
								top: this.timeToPixels(shift.from),
								height: this.hoursToPixels(shift.to - shift.from)
							};

							return (<Shift key={ 'shift' + shift.from }
							               shift={ shift }
							               onClick={ this.props.onShiftClick}

							               className={ styles.shift }
							               style={ style } />
							)
						})}
					</div>
				</div>
				{ map(timeslots, ( slot ) => {
					const style = this.getSlotColorStyle(slot);

					return (<div key={ 'slot' + slot.from } className={ styles.timeslotWrapper } onClick={ this.addShift(slot.from) }>
						<div className={ styles.timeslot } style={ style }></div>
					</div>)
				})}
			</div>
		);
	}
}

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(CalanderDate);
