import React, {PropTypes} from 'react';


import styles from './Shift.css';

/**
 * @class Shift
 * @module *
 */
class Shift extends React.Component {
	handleClick = () => {
		this.props.onClick(this.props.shift);
	}

	render = () => {
		const { style, shift: { to, from, location: { nafn }}, className } = this.props;

		return (
			<div className={ styles.wrapper } style={ style }>
				<div className={ [styles.main, className].join(' ') } onClick={ this.handleClick }>
					<div className={ styles.info }>Frá kl { from } til kl { to }</div>
					<div className={ styles.info }>{ nafn }</div>
				</div>
			</div>
		);
	}
}

export default Shift;
