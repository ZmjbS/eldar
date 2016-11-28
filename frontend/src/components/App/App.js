import React, {Component} from 'react';
import Header from '../Header/Header';
import Calendar from '../Calendar/Calander';
import Box from '../Box/Box';
import Options from '../Options/Options';
import styles from './App.css';
import '../../styles/main.css';

class App extends Component {

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
		return (
			<Box flow>
				<Header />
				<div>
					<Options shiftBackground={this.state.showShiftBackground} onToggleShiftBackground={this.setShiftBackground} />
					<Calendar data={ this.state.data}
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

export default App;
