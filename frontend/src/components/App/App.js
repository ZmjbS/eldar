import React, {Component} from 'react';
import {connect} from 'react-redux'
import {isEqual} from 'lodash';
import Header from '../Header/Header';
import Calendar from '../Calendar/Calander';
import Box from '../Box/Box';
import Options from '../Options/Options';
import styles from './App.css';
import {getTimeSlotsForStore} from '../../actions/timeslotsActions';
import {getUserByEmail} from '../../actions/userActions';
import {save, loadShifts} from '../../actions/shiftsActions';
import {fetchLocations} from '../../actions/locationsActions';
import {getTimeslotsForeStoreGroupedByDays} from '../../selectors/timeslotSelectors';
import {getShiftsTimeslotIds} from '../../selectors/shiftsSelector';
import '../../styles/main.css';

const mapStateToProps = ( state, props ) => {
	return {
		currentUser: state.users.currentUser,
		email: props.params.email,
		timeslots: getTimeslotsForeStoreGroupedByDays(state, props),
		shifts: getShiftsTimeslotIds(state, props),
		skraning: state.shifts.skraning,
		loadingSkraning: state.shifts.loadingSkraning,
		doneLoading: state.shifts.loaded,
		locations: state.locations.list
	}
}

const mapDispatchToProps = ( dispatch ) => {
	return {
		loadTimeslots: ( storeId ) => dispatch(getTimeSlotsForStore(storeId)),
		loadUser: ( email ) => dispatch(getUserByEmail(email)),
		saveShifts: ( shiftsIds, userId ) => dispatch(save(shiftsIds, userId)),
		loadShifts: ( userId ) => dispatch(loadShifts(userId)),
		loadLocations: () => dispatch(fetchLocations()),
	}
}

class App extends Component {

	componentWillMount = () => {
		console.log('foo', !this.props.timeslots || this.props.timeslots.length === 0);
		if ( !this.props.currentUser ) {
			this.props.loadUser(this.props.email)
				.then(this.loadtimeslots);
			//this.props.router.push('/');
		} else if ( !this.props.timeslots || this.props.timeslots.length === 0 ) {
			console.log('JO');
			this.loadtimeslots();
		}

		if ( this.props.locations.length === 0 ) {
			this.props.loadLocations();
		}

		if ( !this.props.skraning && this.props.currentUser ) {
			this.props.loadShifts(this.props.currentUser.id);
		}
	}

	loadtimeslots = () => {
		this.props.loadTimeslots()
	}

	componentWillReceiveProps = ( nextProps ) => {
		if ( this.props.doneLoading && !isEqual(nextProps.shifts, this.props.shifts) ) {
			this.props.saveShifts(nextProps.shifts, nextProps.currentUser.id);
			setTimeout(this.props.loadTimeslots, 2000);
		}

		if ( !nextProps.loadingSkraning && !nextProps.skraning && nextProps.currentUser ) {
			this.props.loadShifts(nextProps.currentUser.id);
		}
	}

	state = {
		showShiftBackground: true,
		day: 0,
	}

	setShiftBackground = ( show ) => {
		this.setState({
			showShiftBackground: show
		})
	};

	nextDay = () => {
		console.log('NEXT');
		if ( this.state.day < 4 )
			this.setState({
				day: this.state.day + 1
			});
	}

	prevDay = () => {
		if ( this.state.day > 0 )
			this.setState({
				day: this.state.day - 1
			});
	}

	render () {
		if ( !this.props.timeslots || this.props.timeslots.length === 0 ) {
			return (<Box />);
		}

		return (
			<Box flow>
				<Header />
				<div>
					<Options shiftBackground={this.state.showShiftBackground} onToggleShiftBackground={this.setShiftBackground} />
					<Calendar data={ this.state.data}
					          timeslots={ this.props.timeslots }
					          showShiftBackground={this.state.showShiftBackground}
					          onChange={ this.onShiftChange }
					          day={ this.state.day }
					          numberOfDays={ 5 }
					          onPrevDay={ this.prevDay }
					          onNextDay={ this.nextDay }
					/>
				</div>
			</Box>
		);
	}
}
export default connect(mapStateToProps, mapDispatchToProps)(App);
