import React, { PropTypes } from 'react';
import styles from './Header.css';

/**
 * @class Header
 * @module *
 */
class Header extends React.Component {

	//static defaultProps = {};
	//static propTypes = {};
	//state = {};

	//componentWillMount () {}
	//componentDidMount () {}
	//componentWillUnmount () {}
	//shouldComponentMount () { return true; }

	render () {
		return (
			<div className={ styles.main }>
				<h1 className={ styles.title }>
					Vaktaskráningarkerfi HSSR
				</h1>
				<div className={ styles.user}>
					Baldur Árnason - baldurarna@gmail.com
				</div>
			</div>
		);
	}
}

export default Header;
