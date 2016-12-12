import React, { PropTypes } from 'react';
import {connect} from 'react-redux'
import styles from './Header.css';

const mapStateToProps = ( state, props ) => {
	return {
		currentUser: state.users.currentUser
	}
}

const mapDispatchToProps = ( dispatch ) => {
	return {
	}
}


class Header extends React.Component {

	//static defaultProps = {};
	//static propTypes = {};
	//state = {};

	//componentWillMount () {}
	//componentDidMount () {}
	//componentWillUnmount () {}
	//shouldComponentMount () { return true; }

	render () {
		const { currentUser: { nafn, netfang, simi }} = this.props;

		return (
			<div className={ styles.main }>
				<h1 className={ styles.title }>
					Vaktaskráningarkerfi HSSR
				</h1>
				<div className={ styles.user}>
					{ nafn } - { netfang } - { simi }
				</div>
			</div>
		);
	}
}

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(Header);

