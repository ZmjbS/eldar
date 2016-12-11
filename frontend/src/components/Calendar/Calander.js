import React, {PropTypes} from 'react';
import map from 'lodash/map';
import throttle from 'lodash/throttle';
import maxBy from 'lodash/maxBy';
import minBy from 'lodash/minBy';
import Swipeable from 'react-swipeable';
import {connect} from 'react-redux'
import CalanderDate from '../Date/CalanderDate';
import TimeScale from '../Date/TimeScale';
import ShiftEdit from '../Shift/ShiftEdit';
import { getTimeslotsForDate } from '../../utils/timeslots';
import { getShiftsForDate, getNextFullShift, getPrevFullShift } from '../../utils/shifts';

import styles from './Calendar.css';

const mapStateToProps = ( state, props ) => {
	return {
		shifts: state.shifts.list
	}
}

const mapDispatchToProps = ( dispatch ) => {
	return {
	}
}

/**
 * @class Calander
 * @module *
 */
class Calander extends React.Component {

	state = {
		width: 0
	}

	componentDidMount = () => {
		this.calculateWidth();

		this.resizeListener = throttle(this.calculateWidth, 50);
		window.addEventListener('resize', this.resizeListener);
	}

	calculateWidth = () => {
		this.setState({
			width: this._containerEl.getBoundingClientRect().width
		});
	};

	editShift = ( shift ) => {
		this.setState({
			editShift: shift
		})
	}

	closeEdit = () => {
		this.setState({
			editShift: null
		})
	}

	renderEdit = () => {
		const { editShift } = this.state;

		if(!editShift) return;

		return (
			<ShiftEdit shift={ editShift }
			           onClose={ this.closeEdit }
			           timeslots={ this.props.timeslots }
			           date={ editShift.date }
			/>
		)
	}

	render () {
		const { width } = this.state;
		const { day, numberOfDays, timeslots, showShiftBackground, onChange } = this.props;

		const style = {};

		if ( width <= 480 ) {
			const translateX = -width * (day);
			const wrapperWidth = numberOfDays * 100;
			style.transform = `translateX(${translateX}px)`;
			style.width = `(${wrapperWidth}%)`;
		}

		return (
			<div>
				{ this.renderEdit() }
				<div className={ styles.main }>
					<TimeScale className={ styles.timescale } timeslots={ timeslots ? timeslots[0].data : []} />

					<div className={ styles.calanderDatesWrapper } ref={( c ) => this._containerEl = c}>
						<Swipeable onSwipedRight={this.props.onPrevDay } onSwipedLeft={ this.props.onNextDay }>
							<div className={ styles.calanderDatesSlider } style={ style }>
								{ map(timeslots, ( date ) => {
									return (<CalanderDate
										key={ 'date' + date.date.toString() }
										date={ date.date }
										className={ styles.date }
										showShiftBackground={showShiftBackground}
										onChange={ onChange }
										onPrevDay={ this.props.onPrevDay }
										onNextDay={ this.props.onNextDay }
										onShiftClick={ this.editShift }
									    timeslots={ this.props.timeslots }
									/>)
								})}
							</div>
						</Swipeable>
					</div>

				</div>
			</div>
		);
	}
}

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(Calander);
