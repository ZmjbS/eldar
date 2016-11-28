import React, { PropTypes } from 'react';
import styles from './Options.css';
/**
 * @class Options
 * @module *
 */
class Options extends React.Component {

	static defaultProps = {
		shiftBackground: true,
		onToggleShiftBackground: () => {}
	};
	static propTypes = {
		shiftBackground: PropTypes.bool,
		onToggleShiftBackground: PropTypes.func
	};
	//state = {};

	//componentWillMount () {}
	//componentDidMount () {}
	//componentWillUnmount () {}
	//shouldComponentMount () { return true; }

	toggleTurnOfBackground = () => {
		this.props.onToggleShiftBackground(!this.props.shiftBackground);
	}

	render () {
		return (
			<div className={ styles.main }>
				<div className={ styles.turnOffBackground} onClick={ this.toggleTurnOfBackground}>Slökkva á vaktaþörf</div>
			</div>
		);
	}
}

export default Options;
