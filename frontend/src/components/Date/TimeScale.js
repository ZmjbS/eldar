import React, {PropTypes} from 'react';
import map from 'lodash/map';

import styles from './TimeScale.css';

/**
 * @class TimeScale
 * @module *
 */
class TimeScale extends React.Component {

	render () {
		const { timeslots } = this.props;
		return (
			<div className={ [styles.main, this.props.className].join(' ') }>
				<div className={ styles.head }></div>
				{ map(timeslots, ( slot ) => {
					return (<div key={ 'slot' + slot.from } className={ styles.timeslot }>
						{ slot.from }
					</div>)
				})}
			</div>
		);
	}
}

export default TimeScale;
