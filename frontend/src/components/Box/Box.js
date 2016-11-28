'use strict';

import React, {PropTypes} from 'react';
import styles from './Box.css';
/**
 * @class Box
 * @module *
 */
class Box extends React.Component {

	render () {
		return (
			<div className={ styles.wrapper}>
				<div className={styles.main }>


				</div>
				<div className={  this.props.flow ? styles.boxFlow : styles.box}>
					{ this.props.children }
				</div>
			</div>
		);
	}
}

export default Box;
